import io
import xml.etree.ElementTree as ElementTree

import resvg_py
from PIL import Image

from src.domain.enums.crop_method import CropMethod
from src.domain.enums.image_format import ImageFormat
from src.domain.exceptions import InvalidImageError
from src.domain.models.cropped_image import CroppedImage
from src.domain.models.image_size import ImageSize

_SVG_NAMESPACE = "http://www.w3.org/2000/svg"
_XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"


class ResvgVectorImageCropper:
    def crop(self, content: bytes) -> CroppedImage:
        rendered = self._render(content)
        root = self._parse(content)
        min_x, min_y, view_width, view_height = self._read_view_box(root, rendered)
        original_size = ImageSize(round(view_width), round(view_height))

        bounds = rendered.getbbox()
        if not bounds or not rendered.width or not rendered.height:
            return self._unchanged(content, original_size)

        left, top, right, bottom = bounds
        scale_x = view_width / rendered.width
        scale_y = view_height / rendered.height

        cropped_x = min_x + left * scale_x
        cropped_y = min_y + top * scale_y
        cropped_width = (right - left) * scale_x
        cropped_height = (bottom - top) * scale_y

        root.set("viewBox", f"{cropped_x:g} {cropped_y:g} {cropped_width:g} {cropped_height:g}")
        # An SVG carrying only a viewBox has an intrinsic ratio but no intrinsic size, so it
        root.set("width", f"{cropped_width:g}")
        root.set("height", f"{cropped_height:g}")

        return CroppedImage(
            content=ElementTree.tostring(root, encoding="utf-8", xml_declaration=True),
            original_size=original_size,
            cropped_size=ImageSize(round(cropped_width), round(cropped_height)),
            crop_method=CropMethod.SVG,
            output_format=ImageFormat.SVG,
        )

    @staticmethod
    def _render(content: bytes) -> Image.Image:
        try:
            png = bytes(resvg_py.svg_to_bytes(svg_string=content.decode("utf-8")))
            return Image.open(io.BytesIO(png)).convert("RGBA")
        except Exception as error:
            raise InvalidImageError("The uploaded file could not be rendered as SVG") from error

    @staticmethod
    def _parse(content: bytes) -> ElementTree.Element:
        ElementTree.register_namespace("", _SVG_NAMESPACE)
        ElementTree.register_namespace("xlink", _XLINK_NAMESPACE)
        try:
            return ElementTree.fromstring(content)
        except ElementTree.ParseError as error:
            raise InvalidImageError("The uploaded file is not valid SVG") from error

    @staticmethod
    def _read_view_box(
        root: ElementTree.Element,
        rendered: Image.Image,
    ) -> tuple[float, float, float, float]:
        view_box = root.get("viewBox")
        if not view_box:
            # Without a viewBox the user units are CSS pixels, which is what resvg rendered at.
            return 0.0, 0.0, float(rendered.width), float(rendered.height)

        values = [float(value) for value in view_box.replace(",", " ").split()]
        if len(values) != 4:
            raise InvalidImageError("The SVG viewBox is malformed")
        return values[0], values[1], values[2], values[3]

    @staticmethod
    def _unchanged(content: bytes, size: ImageSize) -> CroppedImage:
        return CroppedImage(
            content=content,
            original_size=size,
            cropped_size=size,
            crop_method=CropMethod.SVG,
            output_format=ImageFormat.SVG,
        )
