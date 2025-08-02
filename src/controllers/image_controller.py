from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from src.services.image_service import auto_crop_image
import base64
import io
import os

router = APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    templates = request.app.state.templates
    environment = os.environ.get('FLASK_ENV', 'unknown')
    version = os.environ.get('APP_VERSION', 'unknown')
    version_url = f"https://github.com/Pianonic/CropTransparent/releases/tag/{version}"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "environment": environment,
        "version": version,
        "version_url": version_url
    })

@router.get("/about", response_class=HTMLResponse, include_in_schema=False)
def about(request: Request):
    templates = request.app.state.templates
    environment = os.environ.get('FLASK_ENV', 'unknown')
    version = os.environ.get('APP_VERSION', 'unknown')
    version_url = f"https://github.com/Pianonic/CropTransparent/releases/tag/{version}"
    return templates.TemplateResponse("about.html", {
        "request": request,
        "environment": environment,
        "version": version,
        "version_url": version_url
    })

@router.get("/api/app-info", tags=["App Info"])
def app_info():
    environment = os.environ.get('FLASK_ENV', 'unknown environment')
    version = os.environ.get('APP_VERSION', 'unknown version')
    return {"environment": environment, "version": version}

@router.post("/api/process", tags=["Image Processing"])
async def process_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file part")
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")
    try:
        image_data = await file.read()
        output_buffer, original_size, cropped_size, crop_method, background_info, output_format = auto_crop_image(image_data)
        encoded = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        output_buffer.seek(0)
        filename = file.filename or 'image.png'
        original_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'png'
        if output_format:
            extension = output_format.lower()
            if extension == 'jpeg':
                extension = 'jpg'
        else:
            if original_extension not in ['png', 'gif', 'webp', 'jpg', 'jpeg']:
                extension = 'png'
            else:
                extension = original_extension
                if extension == 'jpeg':
                    extension = 'jpg'
        mime_type = 'png'
        if extension == 'jpg':
            mime_type = 'jpeg'
        elif extension in ['gif', 'webp']:
            mime_type = extension
        base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
        output_filename = f"cropped_{base_name}.{extension}"
        response_data = {
            "success": True,
            "image": f"data:image/{mime_type};base64,{encoded}",
            "filename": output_filename,
            "original_size": f"{original_size[0]}x{original_size[1]}",
            "cropped_size": f"{cropped_size[0]}x{cropped_size[1]}",
            "crop_method": crop_method,
            "output_format": extension
        }
        if background_info:
            response_data["background_color"] = background_info
        return JSONResponse(content=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/download", tags=["Image Processing"])
async def download_image(data: dict):
    try:
        if not data or 'image' not in data or 'filename' not in data:
            raise HTTPException(status_code=400, detail="Missing data")
        image_data = data['image'].split(',')[1]
        image_binary = base64.b64decode(image_data)
        output = io.BytesIO(image_binary)
        output.seek(0)
        filename = data['filename']
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'png'
        mime_type_map = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        mime_type = mime_type_map.get(extension, 'image/png')
        return StreamingResponse(output, media_type=mime_type, headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def register_routes(app):
    app.include_router(router)