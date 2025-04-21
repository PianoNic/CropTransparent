# <p align="center">CropTransparent</p>
<p align="center">
  <img src="assets/CropTransparentBorder.png" width="200" alt="CropTransparent Logo">
</p>
<p align="center">
  <strong>A modern, lightweight web application for automatically cropping transparent areas from PNG, GIF, and WEBP images.</strong>
  Built with Flask and containerized with Docker for easy deployment.
</p>
<p align="center">
  <a><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FPianonic%2FCropTransparent&count_bg=%234667e3&title_bg=%23555555&icon=eye.svg&icon_color=%23E7E7E7&title=Visits&edge_flat=false"/></a>
  <a href="https://github.com/Pianonic/CropTransparent/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Pianonic/CropTransparent?color=4667e3&label=License"/></a>
  <a href="https://github.com/Pianonic/CropTransparent/releases"><img src="https://img.shields.io/github/v/release/Pianonic/CropTransparent?include_prereleases&color=4667e3&label=Latest%20Release"/></a>
  <a href="https://github.com/Pianonic/CropTransparent?tab=readme-ov-file#-installation"><img src="https://img.shields.io/badge/Selfhost-Instructions-4667e3.svg"/></a>
</p>

## 🚀 Features
- **Fast In-Memory Processing**: Images are processed in memory without saving to disk
- **Mobile-Friendly UI**: Responsive design that works on all devices
- **Drag & Drop Interface**: Easy to use with drag and drop or file selection
- **Instant Preview**: See the results immediately before downloading
- **Size Comparison**: View the original and cropped dimensions with saved space calculation
- **Docker Ready**: Easy deployment with Docker and Docker Compose

## 📸 Screenshots
<p align="center">
  <img src="/assets/Screenshot1.png" width="800" alt="CropTransparent Screenshot 1"><br/>
  <img src="/assets/Screenshot2.png" width="800" alt="CropTransparent Screenshot 2">
</p>

## 📦 Installation

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Pianonic/CropTransparent.git
cd CropTransparent

# Start with Docker Compose
docker compose up -d
```
The application will be available at [http://localhost:3784](http://localhost:3784)

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

## 💻 Development
To contribute to this project:

1.  Fork the repository on GitHub.
2.  Create a feature branch: `git checkout -b feature/your-amazing-feature`
3.  Make your changes and commit them: `git commit -m 'Add your amazing feature'`
4.  Push your changes to your fork: `git push origin feature/your-amazing-feature`
5.  Open a Pull Request on the original repository.

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
See the [LICENSE](LICENSE) file for more details.

---
<p align="center">Made with ❤️ by <a href="https://github.com/Pianonic">Pianonic</a></p>
