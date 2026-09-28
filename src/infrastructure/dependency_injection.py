from mediatorx import DictResolver, Mediator

from src.application.commands.crop_image.crop_image_command import CropImageCommand
from src.application.commands.crop_image.crop_image_command_handler import (
    CropImageCommandHandler,
)
from src.application.queries.get_application_info.get_application_info_query import (
    GetApplicationInfoQuery,
)
from src.application.queries.get_application_info.get_application_info_query_handler import (
    GetApplicationInfoQueryHandler,
)
from src.infrastructure.configuration.environment_application_info_provider import (
    EnvironmentApplicationInfoProvider,
)
from src.infrastructure.imaging.pillow_raster_image_cropper import PillowRasterImageCropper
from src.infrastructure.imaging.resvg_vector_image_cropper import ResvgVectorImageCropper


def build_mediator() -> Mediator:
    raster_cropper = PillowRasterImageCropper()
    vector_cropper = ResvgVectorImageCropper()
    info_provider = EnvironmentApplicationInfoProvider()

    resolver = DictResolver()
    resolver.add_instance(
        CropImageCommandHandler,
        CropImageCommandHandler(raster_cropper, vector_cropper),
    )
    resolver.add_instance(
        GetApplicationInfoQueryHandler,
        GetApplicationInfoQueryHandler(info_provider),
    )

    mediator = Mediator(resolver=resolver)
    mediator.register(CropImageCommand, CropImageCommandHandler)
    mediator.register(GetApplicationInfoQuery, GetApplicationInfoQueryHandler)
    return mediator
