# Self-hosting

CropTransparent is a single stateless container. Nothing is written to disk, so there is no volume to mount.

## Docker Compose (recommended)

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

## Docker

```bash
docker run -p 5000:5000 ghcr.io/pianonic/croptransparent:latest
```

## Behind a reverse proxy

The app uses relative URLs throughout, so it works on its own domain or under a sub-path such as `https://example.com/crop/`. Forward the whole path to port 5000.

## Updating

```bash
docker compose pull && docker compose up -d
```

Images are tagged `latest`, `X`, `X.Y` and `X.Y.Z`; pin a major version (e.g. `:1`) to take fixes without breaking changes. See [Configuration](configuration.md) for environment variables.
