# <p align="center">CropTransparent</p> 
<p align="center">
  <img src="https://raw.githubusercontent.com/Pianonic/CropTransparent/main/assets/CropTransparentBorder.png" width="200" alt="CropTransparent Logo">
</p>
<p align="center">
  <strong>A lightweight web app for automatically cropping images - removes transparent areas and uniform backgrounds.</strong>
  Built with Flask and Docker.
</p>
<p align="center">
  <a href="https://github.com/Pianonic/CropTransparent"><img src="https://badgetrack.pianonic.ch/badge?tag=crop-transparent&label=visits&color=f87171&style=flat" alt="visits" /></a>
  <a href="https://github.com/Pianonic/CropTransparent/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Pianonic/CropTransparent?color=f87171&label=License"/></a>
  <a href="https://github.com/Pianonic/CropTransparent/releases"><img src="https://img.shields.io/github/v/release/Pianonic/CropTransparent?include_prereleases&color=f87171&label=Latest%20Release"/></a>
  <a href="https://github.com/Pianonic/CropTransparent?tab=readme-ov-file#-installation"><img src="https://img.shields.io/badge/Selfhost-Instructions-f87171.svg"/></a>
</p>

## 🚀 Features
- **Smart Cropping**: Auto-crops transparency (PNG, GIF, WEBP) or uniform backgrounds (JPEG)
- **Multiple Formats**: PNG, JPEG, GIF, WEBP support
- **Fast Processing**: In-memory processing, no disk storage
- **Drag & Drop**: Simple file upload interface
- **Format Preservation**: JPEG stays JPEG, PNG stays PNG
- **Docker Ready**: Easy deployment

## 📸 Screenshots (Light and Darkmode)
<p align="center">
  <img src="/assets/showcase/home.png" width="800" alt="CropTransparent Homepage"><br/><br/>
  <img src="/assets/showcase/processed.png" width="800" alt="CropTransparent Processed Page"><br/>
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
docker run -d -p 5000:5000 --name croptransparent pianonic/croptransparent:latest
```
The application will be available at [http://localhost:5000](http://localhost:5000).

#### Option 2: Run with Docker Compose
**1. Create a `compose.yaml` file:**  
Use your favorite editor to create a `compose.yaml` file and paste this into it:
```yaml
services:
  croptransparent:
    image: pianonic/croptransparent:latest # Uses the image from Docker Hub
    # image: ghcr.io/pianonic/croptransparent:latest # Uses the image from GitHub Container Registry
    ports:
      - "5000:5000"
    restart: unless-stopped
```

**2. Start it:**
```bash
docker compose up -d
```
The application will be available at [http://localhost:5000](http://localhost:5000).

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
1. Upload an image (drag & drop or browse)
2. App automatically detects and crops transparent areas or uniform backgrounds
3. Preview and download the cropped result

## ⚙️ Technical Details

### Image Processing
Uses PIL/Pillow and NumPy for smart cropping:
- **Transparent images**: Crops based on alpha channel
- **Opaque images**: Detects uniform background from corners and crops
- **Security**: All processing in memory, no files saved to disk

## 📋 Requirements
- Python 3.13+
- Docker
- Dependencies: Shown in [requirements.txt](./requirements.txt)

## 📜 License
This project is licensed under the MIT License.
See the [LICENSE](https://github.com/Pianonic/CropTransparent/blob/main/LICENSE) file for more details.

---
<p align="center">Made with ❤️ by <a href="https://github.com/Pianonic">Pianonic</a></p>
