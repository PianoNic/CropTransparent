<p align="center">
  <img src="assets/CropTransparentBorder.png" width="160" alt="CropTransparent Logo">
</p>

<h1 align="center">CropTransparent</h1>

<p align="center">
  <strong>Trims the empty edges off your images: transparent borders, flat backgrounds, and empty SVG space.</strong>
</p>

<p align="center">
  <a href="https://github.com/PianoNic/CropTransparent"><img src="https://badgetrack.pianonic.ch/badge?tag=crop-transparent&label=visits&color=2d6a4f&style=flat" alt="visits"/></a>
  <a href="https://github.com/PianoNic/CropTransparent/blob/main/LICENSE"><img src="https://img.shields.io/github/license/PianoNic/CropTransparent?color=2d6a4f&label=License" alt="License"/></a>
  <a href="https://github.com/PianoNic/CropTransparent/releases"><img src="https://img.shields.io/github/v/release/PianoNic/CropTransparent?include_prereleases&color=2d6a4f&label=Latest%20Release" alt="Latest release"/></a>
  <a href="#installation"><img src="https://img.shields.io/badge/Selfhost-Instructions-2d6a4f.svg" alt="Self-hosting"/></a>
</p>

## Screenshots

<p align="center">
  <img src="assets/screenshots/home-light.png" width="49%" alt="Empty cutting mat, light mode" />
  <img src="assets/screenshots/results-light.png" width="49%" alt="Three cropped images, light mode" />
</p>
<p align="center">
  <img src="assets/screenshots/home-dark.png" width="49%" alt="Empty cutting mat, dark mode" />
  <img src="assets/screenshots/results-dark.png" width="49%" alt="Three cropped images, dark mode" />
</p>

<details>
<summary><strong>Mobile</strong></summary>

<p align="center">
  <img src="assets/screenshots/mobile-dark.png" width="300" alt="Mobile view" />
</p>

</details>

## Features

- **Transparent edges**: PNG, GIF and WEBP are trimmed to the bounds of their alpha channel.
- **Flat backgrounds**: JPEGs and opaque images lose any uniform border detected from the corners, without leaving a compression fringe.
- **Animated images**: every frame of a GIF, WEBP or APNG is cropped to one shared box, so the animation stays intact.
- **SVGs stay vector**: the `viewBox` is tightened to the content, paths are untouched.
- **Batch friendly**: drop, browse or paste (<kbd>Ctrl</kbd>+<kbd>V</kbd>) several images at once, then download one or all as a ZIP.
- **Private**: images are processed in memory and never written to disk.
- **API**: everything the UI does is a single `POST /api/process`, documented at `/docs`.

## Installation

### Docker Compose (recommended)

Create a `compose.yml`:

```yaml
services:
  crop-transparent:
    image: pianonic/croptransparent:latest # Docker Hub
    # image: ghcr.io/pianonic/croptransparent:latest # GitHub Container Registry
    ports:
      - "5000:5000"
    restart: unless-stopped
```

```bash
docker compose up -d
```

Open <http://localhost:5000>.

### Docker

```bash
docker run -p 5000:5000 ghcr.io/pianonic/croptransparent:latest
```

### From source

Requires Python 3.11+ and Node 22+.

```bash
cd frontend && npm install && npm run build && cd ..
pip install -r requirements.txt
python asgi.py
```

For frontend work, run `npm run dev` in `frontend/` next to `python asgi.py`; Vite proxies `/api` to port 5000.

Run the tests with `python -m pytest tests`.

<details>
<summary><strong>Tech stack</strong></summary>

- **Backend**: Python + FastAPI, Pillow + NumPy for raster images, resvg for SVG rasterisation, [mediatorx](https://pypi.org/project/mediatorx/) for CQRS.
- **Frontend**: [Preact](https://preactjs.com) + [Lucide](https://lucide.dev) icons, built with Vite and served by FastAPI as a SPA.
- **Architecture**: onion; dependencies point inwards only.

```
src/
  domain/          enums, models and exceptions - no framework dependencies
  application/     use cases as commands and queries, plus the ports they need
  infrastructure/  Pillow / resvg / environment adapters + the composition root
  api/             FastAPI controllers, which only build a message and send it
frontend/          Preact SPA; npm run build emits frontend/dist, served at /
```

</details>

## License

[MIT](LICENSE)
