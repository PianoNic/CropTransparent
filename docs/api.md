# API

Everything the web app does goes through one endpoint. Interactive docs are served at `/docs`.

## `POST /api/process`

Multipart form with one field, `file`.

```bash
curl -F "file=@logo.png" http://localhost:5000/api/process
```

```json
{
  "success": true,
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "filename": "cropped_logo.png",
  "original_size": "400x400",
  "cropped_size": "267x310",
  "crop_method": "transparent",
  "output_format": "png"
}
```

| Field | Description |
|---|---|
| `image` | The cropped file as a data URI. |
| `crop_method` | `transparent`, `color_background` or `svg`. |
| `output_format` | Same format as the upload; a still image with transparency becomes `png`. |
| `background_color` | Only for `color_background`: the detected colour as `[r, g, b]`. |

| Status | Meaning |
|---|---|
| `400` | No file or an empty file. |
| `413` | Over one of the [limits](configuration.md#limits). |
| `422` | Not a readable image. |
| `503` | Too many crops waiting; retry after the `Retry-After` seconds. |

## `GET /api/app-info`

```json
{ "environment": "production", "version": "1.5.0" }
```
