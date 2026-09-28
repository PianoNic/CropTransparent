# CropTransparent

Automatically crops images by removing transparent areas and uniform backgrounds.

## Features

- Removes transparent areas (PNG, GIF, WEBP)
- Removes uniform/solid backgrounds (JPEG)
- Tightens SVG viewBox to the content bounds (stays vector)
- Drag-and-drop upload
- In-memory processing — no files saved to disk
- Light and dark mode

## Screenshots

<p align="center">
  <img src="/assets/home.png" width="800" alt="CropTransparent Homepage"><br/><br/>
  <img src="/assets/processed.png" width="800" alt="CropTransparent Processed Page"><br/>
</p>

## Tech Stack

- Python 3.11+ (3.13 in Docker) + FastAPI
- Pillow + NumPy for raster processing, resvg for SVG rasterisation
- [mediatorx](https://pypi.org/project/mediatorx/) for CQRS command/query dispatch
- Docker support

## Architecture

Onion architecture; dependencies point inwards only.

```
src/
  domain/          enums, models and exceptions - no framework dependencies
  application/     use cases as commands and queries, plus the ports they need
    commands/      crop_image
    queries/       get_application_info
    abstractions/  IRasterImageCropper, IVectorImageCropper, IApplicationInfoProvider
  infrastructure/  Pillow / resvg / environment adapters + the composition root
  api/             FastAPI controllers, which only build a message and send it
```

Controllers never touch imaging code. They construct a `CropImageCommand` or a
`GetApplicationInfoQuery` and hand it to the mediator; `build_mediator()` in
`src/infrastructure/dependency_injection.py` is the single place that wires
handlers to their implementations.

## Run with Docker

```bash
docker run -p 5000:5000 ghcr.io/pianonic/croptransparent:latest
```

Or with Docker Compose:

```bash
docker compose up
```

## Run Manually

```bash
pip install -r requirements.txt
python asgi.py
```

Requires Python 3.11 or newer (`mediatorx` needs `StrEnum`).

Run the checks with:

```bash
python tests/test_cropping.py
```

Open `http://localhost:5000`.

## License

[MIT](LICENSE)