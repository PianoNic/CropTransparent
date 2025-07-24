# <p align="center">CropTransparent</p> 
<p align="center">
  <img src="https://raw.githubusercontent.com/Pianonic/CropTransparent/main/assets/CropTransparentBorder.png" width="200" alt="CropTransparent Logo">
</p>
<p align="center">
  <strong>A modern, lightweight web application for automatically cropping transparent areas from PNG, GIF, and WEBP images.</strong>
  Built with Flask and containerized with Docker for easy deployment.
</p>
<p align="center">
  <a href="https://github.com/Pianonic/CropTransparent"><img src="https://badgetrack.pianonic.ch/badge?url=https://github.com/PianoNic/CropTransparent&label=visitors&color=f87171&style=flat&logo=github" alt="Visitor badge"/></a>
  <a href="https://github.com/Pianonic/CropTransparent/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Pianonic/CropTransparent?color=f87171&label=License"/></a>
  <a href="https://github.com/Pianonic/CropTransparent/releases"><img src="https://img.shields.io/github/v/release/Pianonic/CropTransparent?include_prereleases&color=f87171&label=Latest%20Release"/></a>
  <a href="https://github.com/Pianonic/CropTransparent?tab=readme-ov-file#-installation"><img src="https://img.shields.io/badge/Selfhost-Instructions-f87171.svg"/></a>
</p>

## 🚀 Features
- **Fast In-Memory Processing**: Images are processed in memory without saving to disk
- **Drag & Drop Interface**: Easy to use with drag and drop or file selection
- **Instant Preview**: See the results immediately before downloading
- **Size Comparison**: View the original and cropped dimensions with saved space calculation
- **Docker Ready**: Easy deployment with Docker and Docker Compose

## 📸 Screenshots (Light and Darkmode)
<p align="center">
  <img src="https://raw.githubusercontent.com/Pianonic/CropTransparent/main/assets/showcase/home.png" width="800" alt="CropTransparent Homepage"><br/><br/>
  <img src="https://raw.githubusercontent.com/Pianonic/CropTransparent/main/assets/showcase/processed.png" width="800" alt="CropTransparent Processed Page"><br/>
</p>

## 📦 Installation

### Using Docker (Recommended)

#### Option 1: Pull and Run a Pre-built Image
You can pull the latest pre-built image from Docker Hub or GitHub Container Registry.

**Docker Hub:**
```bash
docker pull pianonic/croptransparent:latest
```

**GitHub Container Registry:**
```bash
docker pull ghcr.io/pianonic/croptransparent:latest
```

Then, run the container:
```bash
docker run -d -p 3784:5000 --name croptransparent pianonic/croptransparent:latest
```
The application will be available at [http://localhost:3784](http://localhost:3784).

#### Option 2: Build and Run with Docker Compose
This method builds the image locally from the source code.

**1. Clone the repository:**
```bash
git clone https://github.com/Pianonic/CropTransparent.git
cd CropTransparent
```

**2. Start with Docker Compose:**
```bash
docker compose up -d
```
The application will be available at [http://localhost:3784](http://localhost:3784).

A `docker-compose.yml` file like this is used:
```yaml
# docker-compose.yml
version: "3.8"

services:
  croptransparent:
    build: .
    image: pianonic/croptransparent
    ports:
      - "3784:5000"
    restart: unless-stopped
```

The container is built using a `Dockerfile`:
```dockerfile
# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "wsgi.py"]
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/Pianonic/CropTransparent.git
cd CropTransparent

# Create a virtual environment
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python wsgi.py
```
The application will be available at [http://localhost:5000](http://localhost:5000) (or the port configured in `wsgi.py`).

## 🛠️ Usage
1.  Upload a transparent image (PNG, GIF, WEBP) by dragging and dropping or using the file browser.
2.  The application automatically finds the bounding box of non-transparent pixels and crops the image.
3.  Preview the cropped result and compare its dimensions to the original.
4.  Download the optimized image with a single click.

## ⚙️ Technical Details

### Image Processing
The application uses the Python Imaging Library (PIL/Pillow) and NumPy to:
1.  Convert images to RGBA format if needed.
2.  Extract the alpha channel.
3.  Find the bounding box of non-transparent pixels using NumPy.
4.  Crop the image to this bounding box using Pillow.
5.  Encode the result and deliver it directly to the user's browser without saving to disk.

### Security
User privacy is prioritized. Uploaded images are processed on the server **entirely in memory**. No original or cropped images are saved to the server's disk. The resulting image is streamed directly back to the user's browser. When the application is self-hosted, images are processed locally and do not leave the user's machine.

## 📋 Requirements
- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- Dependencies listed in `requirements.txt`:
  - Flask
  - Pillow
  - NumPy
  - Waitress (for production WSGI serving)
  - Werkzeug (Flask dependency)

## 📜 License
This project is licensed under the MIT License.
See the [LICENSE](https://github.com/Pianonic/CropTransparent/blob/main/LICENSE) file for more details.

---
<p align="center">Made with ❤️ by <a href="https://github.com/Pianonic">Pianonic</a></p>
