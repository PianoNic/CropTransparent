import base64
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.api.dependencies import MediatorDependency
from src.application.commands.crop_image.crop_image_command import CropImageCommand
from src.application.commands.crop_image.crop_image_command_handler import MAX_UPLOAD_BYTES
from src.domain.exceptions import (
    EmptyUploadError,
    ImageTooLargeError,
    InvalidImageError,
    ServerBusyError,
)
from src.domain.models.cropped_image import CroppedImage

router = APIRouter(prefix="/api", tags=["Image Processing"])


@router.post("/process")
async def process_image(
    mediator: MediatorDependency,
    file: Annotated[UploadFile, File()],
) -> dict[str, object]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No selected file")
    # the multipart body is already spooled to disk; refuse before pulling it into memory
    if file.size is not None and file.size > MAX_UPLOAD_BYTES:
        limit_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        raise HTTPException(status_code=413, detail=f"File too large (max {limit_mb} MB)")

    command = CropImageCommand(
        content=await file.read(),
        file_name=file.filename,
        content_type=file.content_type,
    )

    try:
        result: CroppedImage = await mediator.send(command)
    except EmptyUploadError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except ImageTooLargeError as error:
        raise HTTPException(status_code=413, detail=str(error)) from error
    except InvalidImageError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except ServerBusyError as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"Retry-After": "5"}) from error

    return _to_response(result, file.filename)


def _to_response(result: CroppedImage, source_file_name: str) -> dict[str, object]:
    encoded = base64.b64encode(result.content).decode("utf-8")
    base_name = source_file_name.rsplit(".", 1)[0] if "." in source_file_name else source_file_name
    extension = result.output_format.file_extension

    response: dict[str, object] = {
        "success": True,
        "image": f"data:{result.output_format.media_type};base64,{encoded}",
        "filename": f"cropped_{base_name}.{extension}",
        "original_size": str(result.original_size),
        "cropped_size": str(result.cropped_size),
        "crop_method": result.crop_method.value,
        "output_format": extension,
    }
    if result.background_color is not None:
        response["background_color"] = list(result.background_color.as_tuple())
    return response
