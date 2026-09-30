import asyncio
import os
import sys
import xml.etree.ElementTree as ElementTree
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image

from src.application.commands.crop_image.crop_image_command import CropImageCommand
from src.domain.enums.crop_method import CropMethod
from src.domain.enums.image_format import ImageFormat
from src.domain.exceptions import ImageTooLargeError
from src.domain.models.image_size import ImageSize
from src.infrastructure.dependency_injection import build_mediator
from src.infrastructure.imaging.resvg_vector_image_cropper import ResvgVectorImageCropper

SVG_NS = "http://www.w3.org/2000/svg"

RECT = b"""<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="100" fill="red"/>
</svg>"""

PATH_ONLY = b"""<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
  <path d="M100 100 L300 100 L300 200 Z" fill="blue"/>
</svg>"""

NO_INTRINSIC_SIZE = b"""<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="9" y="10" width="46" height="44" fill="green"/>
</svg>"""

BLANK = b"""<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"></svg>"""


def view_box(content: bytes) -> list[float]:
    return [float(v) for v in ElementTree.fromstring(content).get("viewBox").split()]


def close(actual, expected, tolerance=2.0):
    return all(abs(a - e) <= tolerance for a, e in zip(actual, expected, strict=True))


def png_bytes(size, box, colour=(255, 0, 0, 255)):
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    image.paste(colour, box)
    buffer = BytesIO()
    image.save(buffer, "PNG")
    return buffer.getvalue()


def jpeg_bytes(size, box, colour=(255, 0, 0)):
    image = Image.new("RGB", size, (255, 255, 255))
    image.paste(colour, box)
    buffer = BytesIO()
    image.save(buffer, "JPEG")
    return buffer.getvalue()


def test_vector_cropper():
    cropper = ResvgVectorImageCropper()

    result = cropper.crop(RECT)
    assert result.original_size == ImageSize(200, 200), result.original_size
    assert result.cropped_size == ImageSize(100, 100), result.cropped_size
    assert result.crop_method is CropMethod.SVG
    assert result.output_format is ImageFormat.SVG
    assert close(view_box(result.content), [50, 50, 100, 100]), view_box(result.content)

    root = ElementTree.fromstring(result.content)
    rect = root.find(f"{{{SVG_NS}}}rect")
    assert rect.get("x") == "50" and rect.get("y") == "50", rect.attrib
    assert b"<svg:" not in result.content

    result = cropper.crop(PATH_ONLY)
    assert result.original_size == ImageSize(400, 400), result.original_size
    assert close((result.cropped_size.width, result.cropped_size.height), (200, 100))

    result = cropper.crop(NO_INTRINSIC_SIZE)
    root = ElementTree.fromstring(result.content)
    assert result.cropped_size == ImageSize(46, 44), result.cropped_size
    assert root.get("width") == "46" and root.get("height") == "44", root.attrib

    result = cropper.crop(BLANK)
    assert result.original_size == result.cropped_size == ImageSize(200, 200)
    assert result.content == BLANK


def test_raster_cropping_through_mediator():
    mediator = build_mediator()

    result = asyncio.run(mediator.send(CropImageCommand(png_bytes((200, 200), (50, 50, 150, 150)), "a.png")))
    assert result.crop_method is CropMethod.TRANSPARENT
    assert result.cropped_size == ImageSize(100, 100), result.cropped_size
    assert result.output_format is ImageFormat.PNG

    result = asyncio.run(mediator.send(CropImageCommand(jpeg_bytes((200, 200), (50, 50, 150, 150)), "a.jpg")))
    assert result.crop_method is CropMethod.COLOR_BACKGROUND
    assert close((result.cropped_size.width, result.cropped_size.height), (100, 100), 6)
    assert result.output_format is ImageFormat.JPEG
    assert result.background_color.as_tuple() == (255, 255, 255)


def test_svg_routed_by_extension_and_media_type():
    mediator = build_mediator()

    by_extension = asyncio.run(mediator.send(CropImageCommand(RECT, "logo.SVG")))
    assert by_extension.crop_method is CropMethod.SVG

    by_media_type = asyncio.run(mediator.send(CropImageCommand(RECT, "logo", "image/svg+xml")))
    assert by_media_type.crop_method is CropMethod.SVG


def test_upload_limit_is_enforced():
    mediator = build_mediator()
    oversized = CropImageCommand(b"x" * (26 * 1024 * 1024), "big.png")
    try:
        asyncio.run(mediator.send(oversized))
    except ImageTooLargeError:
        pass
    else:
        raise AssertionError("expected ImageTooLargeError")


def test_domain_helpers():
    assert str(ImageSize(12, 34)) == "12x34"
    assert ImageFormat.JPEG.file_extension == "jpg"
    assert ImageFormat.SVG.media_type == "image/svg+xml"
    assert ImageFormat.from_extension(".JPG") is ImageFormat.JPEG
    assert ImageFormat.from_extension("bmp") is None


def main():
    test_vector_cropper()
    test_raster_cropping_through_mediator()
    test_svg_routed_by_extension_and_media_type()
    test_upload_limit_is_enforced()
    test_domain_helpers()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hero = os.path.join(project_root, "hero-image.svg")
    if os.path.exists(hero):
        with open(hero, "rb") as handle:
            result = ResvgVectorImageCropper().crop(handle.read())
        assert result.cropped_size.area < result.original_size.area
        print(f"hero-image.svg: {result.original_size} -> {result.cropped_size}")

    print("all checks passed")


if __name__ == "__main__":
    main()


def test_animated_gif_keeps_every_frame():
    # content moves between frames; the crop must cover the union and keep the animation
    frames = []
    for box in ((20, 20, 40, 40), (60, 60, 80, 80)):
        frame = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        frame.paste((255, 0, 0, 255), box)
        frames.append(frame)
    buffer = BytesIO()
    frames[0].save(buffer, "GIF", save_all=True, append_images=frames[1:], duration=100, loop=0, disposal=2)

    result = asyncio.run(build_mediator().send(CropImageCommand(buffer.getvalue(), "a.gif")))
    assert result.output_format is ImageFormat.GIF
    assert result.cropped_size == ImageSize(60, 60), result.cropped_size
    assert Image.open(BytesIO(result.content)).n_frames == 2


def test_jpeg_compression_fringe_is_trimmed():
    # saturated colours at low quality bleed a faint fringe well past the base threshold
    for colour in ((20, 120, 200), (250, 200, 0), (0, 200, 0), (255, 0, 0)):
        image = Image.new("RGB", (300, 200), (255, 255, 255))
        image.paste(colour, (100, 50, 200, 150))
        buffer = BytesIO()
        image.save(buffer, "JPEG", quality=40)
        result = asyncio.run(build_mediator().send(CropImageCommand(buffer.getvalue(), "a.jpg")))
        assert close((result.cropped_size.width, result.cropped_size.height), (100, 100), 1), (
            colour,
            result.cropped_size,
        )


def test_spa_fallback_serves_index_but_keeps_api_404s():
    import tempfile
    from pathlib import Path

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from src.api.app import SpaStaticFiles

    dist = Path(tempfile.mkdtemp())
    (dist / "index.html").write_text("<p>spa</p>")
    app = FastAPI()
    app.mount("/", SpaStaticFiles(directory=dist, html=True))
    client = TestClient(app)

    assert client.get("/").text == "<p>spa</p>"
    assert client.get("/some/client/route").text == "<p>spa</p>"
    assert client.get("/api/nope").status_code == 404


def test_flood_is_turned_away_without_blocking_the_event_loop():
    import threading

    from src.application.commands.crop_image.crop_image_command_handler import CropImageCommandHandler
    from src.domain.exceptions import ServerBusyError

    release = threading.Event()

    class SlowCropper:
        def crop(self, _content):
            release.wait(5)
            return "cropped"

    handler = CropImageCommandHandler(SlowCropper(), SlowCropper(), max_concurrent=1, max_pending=2)
    command = CropImageCommand(b"x", "a.png")

    async def flood():
        running = [asyncio.create_task(handler.handle(command)) for _ in range(2)]
        # a blocking crop on the event loop would freeze this sleep until release.set()
        await asyncio.wait_for(asyncio.sleep(0.05), timeout=1)
        try:
            await handler.handle(command)
            raise AssertionError("third request should have been turned away")
        except ServerBusyError:
            pass
        release.set()
        return await asyncio.gather(*running)

    assert asyncio.run(flood()) == ["cropped", "cropped"]


def test_pixel_limits_are_checked_before_decoding():
    from src.domain.exceptions import ImageTooLargeError
    from src.infrastructure.imaging.pillow_raster_image_cropper import PillowRasterImageCropper

    cropper = PillowRasterImageCropper(max_pixels=100 * 100, max_animation_pixels=3 * 50 * 50)

    def raises_too_large(content):
        try:
            cropper.crop(content)
        except ImageTooLargeError:
            return True
        return False

    assert raises_too_large(png_bytes((101, 100), (0, 0, 10, 10)))
    assert not raises_too_large(png_bytes((100, 100), (0, 0, 10, 10)))

    frames = [Image.new("RGBA", (50, 50), (255, 0, 0, i + 1)) for i in range(4)]
    buffer = BytesIO()
    frames[0].save(buffer, "GIF", save_all=True, append_images=frames[1:], duration=100)
    assert raises_too_large(buffer.getvalue())

    svg = ResvgVectorImageCropper(max_render_pixels=1000 * 1000)
    svg_with_size = (
        b'<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s"><rect width="5" height="5"/></svg>'
    )
    huge = svg_with_size % (b"100000", b"100000")
    huge_in_inches = svg_with_size % (b"20in", b"20in")
    for content in (huge, huge_in_inches):
        try:
            svg.crop(content)
            raise AssertionError("oversized SVG should be rejected before rendering")
        except ImageTooLargeError:
            pass
    assert svg.crop(RECT).cropped_size.width < 200


def test_api_rejects_oversized_uploads_and_reports_busy():
    from fastapi.testclient import TestClient

    from src.api.app import create_app
    from src.domain.exceptions import ServerBusyError

    app = create_app()
    client = TestClient(app)

    too_big = b"\0" * (25 * 1024 * 1024 + 1)
    response = client.post("/api/process", files={"file": ("big.png", too_big, "image/png")})
    assert response.status_code == 413, response.text

    class BusyMediator:
        async def send(self, _command):
            raise ServerBusyError("busy")

    app.state.mediator = BusyMediator()
    response = client.post(
        "/api/process", files={"file": ("a.png", png_bytes((10, 10), (0, 0, 5, 5)), "image/png")}
    )
    assert response.status_code == 503
    assert response.headers["retry-after"] == "5"


def test_sentry_stays_off_without_a_dsn_and_scrubs_auth_headers():
    from src.infrastructure.monitoring.sentry_error_reporter import SentryErrorReporter

    assert SentryErrorReporter(None, "test", "0.0.0").initialize() is False
    event = {"request": {"headers": {"Authorization": "Bearer secret", "Accept": "*/*"}}}
    scrubbed = SentryErrorReporter.scrub(event, {})
    assert scrubbed["request"]["headers"] == {"Authorization": "[Filtered]", "Accept": "*/*"}
