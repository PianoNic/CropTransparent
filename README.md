# CropTransparent

Automatically crops images by removing transparent areas and uniform backgrounds.

## Features

- Removes transparent areas (PNG, GIF, WEBP)
- Removes uniform/solid backgrounds (JPEG)
- Drag-and-drop upload
- In-memory processing — no files saved to disk
- Light and dark mode

## Screenshots

<p align="center">
  <img src="/assets/home.png" width="800" alt="CropTransparent Homepage"><br/><br/>
  <img src="/assets/processed.png" width="800" alt="CropTransparent Processed Page"><br/>
</p>

## Tech Stack

- Python 3.13 + FastAPI
- Pillow + NumPy for image processing
- Docker support

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

Open `http://localhost:5000`.

## License

[MIT](LICENSE)