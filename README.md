
# CropTransparent

CropTransparent is a Python tool that crops away the transparent edges of PNG images. It processes images by removing all transparent padding, leaving only the visible content. The resulting image may not be square, but it will be the smallest possible size that contains all non-transparent pixels.

## Features

- Automatically crops transparent edges from PNG images.
- Supports images with an alpha channel (transparency).
- Easy to use with minimal setup.

## Requirements

- Python 3.x
- Pillow
- NumPy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PianoNic/CropTransparent.git
   cd CropTransparent
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your PNG image in the project directory.
2. Run the script with the input and output file paths:
   ```bash
   python crop_transparent.py input.png output.png
   ```

   - Replace `input.png` with the path to your PNG file.
   - Replace `output.png` with the desired output file name.

3. The cropped image will be saved to the specified output path.

### Example

```bash
python crop_transparent.py example.png cropped_example.png
```

If the input image is entirely transparent, the script will notify you and save a copy of the original image.

## How It Works

1. The script loads the PNG image using Pillow.
2. It extracts the alpha (transparency) channel.
3. It identifies the bounding box of all non-transparent pixels.
4. It crops the image to the bounding box and saves the result.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
<p align="center">Made with ❤️ by <a href="https://github.com/Pianonic">PianoNic</a></p>
