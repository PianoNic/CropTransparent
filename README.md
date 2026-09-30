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
  <a href="docs/self-hosting.md"><img src="https://img.shields.io/badge/Selfhost-Instructions-2d6a4f.svg" alt="Self-hosting"/></a>
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

## Quick start

```bash
docker run -p 5000:5000 ghcr.io/pianonic/croptransparent:latest
```

Open <http://localhost:5000>.

## Documentation

- [Self-hosting](docs/self-hosting.md): Docker Compose, Docker and updating
- [Configuration](docs/configuration.md): environment variables and limits
- [API](docs/api.md): cropping images without the UI
- [Development](docs/development.md): running from source, tests and linting
- [Architecture](docs/architecture.md): how the code is organised
- [Releasing](docs/releasing.md): how versions and images are published

## License

[MIT](LICENSE)
