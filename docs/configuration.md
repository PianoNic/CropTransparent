# Configuration

All settings are optional environment variables. A `.env` file next to `asgi.py` is read as well.

| Variable | Default | Description |
|---|---|---|
| `SENTRY_DSN` | not set | Reports server errors (5xx and `ERROR` logs) to Sentry or GlitchTip. Cookies and auth headers are scrubbed. |
| `APP_VERSION` | from `application.properties` | Overrides the version shown in the footer. Normally left unset; releases write it. |
| `APP_ENVIRONMENT` | from `application.properties` | Overrides the environment shown in the footer (`production` in release images). |

## Limits

These protect the server from oversized or malicious uploads. They are constants in the code, not settings.

| Limit | Value | Response |
|---|---|---|
| Upload size | 25 MB | `413` |
| Raster image | 50 megapixels | `413` |
| Animation | 200 million pixels across all frames | `413` |
| SVG render size | 50 megapixels, read from `width`/`height`/`viewBox` before rendering | `413` |
| Crops waiting on the server | 16 | `503` with `Retry-After: 5` |

The web app also uploads at most 3 files at a time and accepts at most 50 files per drop or paste.
