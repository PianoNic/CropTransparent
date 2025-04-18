# CropTransparent

![License](https://img.shields.io/github/license/Pianonic/CropTransparent)
![Version](https://img.shields.io/github/v/release/Pianonic/CropTransparent?include_prereleases)

A modern, lightweight web application for automatically cropping transparent areas from PNG, GIF, and WEBP images. Built with Flask and containerized with Docker for easy deployment.

## Features

- **Fast In-Memory Processing**: Images are processed in memory without saving to disk
- **Mobile-Friendly UI**: Responsive design that works on all devices
- **Drag & Drop Interface**: Easy to use with drag and drop or file selection
- **Instant Preview**: See the results immediately before downloading
- **Size Comparison**: View the original and cropped dimensions with saved space calculation
- **Docker Ready**: Easy deployment with Docker and Docker Compose

## Demo

![CropTransparent Demo](https://raw.githubusercontent.com/Pianonic/CropTransparent/main/docs/demo.gif)

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Pianonic/CropTransparent.git
cd CropTransparent

# Start with Docker Compose
docker compose up -d
```

The application will be available at [http://localhost:5000](http://localhost:5000)

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/Pianonic/CropTransparent.git
cd CropTransparent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python wsgi.py
```

## How It Works

1. Upload a transparent image (PNG, GIF, WEBP) by dragging and dropping or browsing
2. The application finds the bounding box of non-transparent pixels
3. The image is cropped to remove excess transparent areas
4. Preview the result and compare dimensions
5. Download the cropped image with a single click

## Technical Details

### Image Processing

The application uses the Python Imaging Library (PIL/Pillow) and NumPy to:
1. Convert images to RGBA format if needed
2. Extract the alpha channel
3. Find the bounding box of non-transparent pixels
4. Crop the image to this bounding box
5. Deliver the result directly to the user

### Security

- No files are stored on the server
- All processing happens in memory
- Images are transferred directly to the user's browser

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Requirements

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- Dependencies listed in requirements.txt:
  - Flask
  - Pillow
  - NumPy
  - Waitress
  - Werkzeug

## License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/Pianonic/CropTransparent](https://github.com/Pianonic/CropTransparent)

---

Made with ❤️ by [Pianonic](https://github.com/Pianonic)