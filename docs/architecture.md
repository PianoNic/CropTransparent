# Architecture

Onion architecture: dependencies point inwards only, and the API talks to the application exclusively through [mediatorx](https://pypi.org/project/mediatorx/) commands and queries.

```
src/
  domain/          enums, models and exceptions - no framework dependencies
  application/     use cases as commands and queries, plus the ports they need
    commands/      crop_image
    queries/       get_application_info
    abstractions/  IRasterImageCropper, IVectorImageCropper, IApplicationInfoProvider
  infrastructure/  Pillow / resvg adapters, configuration, Sentry, composition root
  api/             class-based FastAPI controllers that build a message and send it
frontend/          Preact SPA; npm run build emits frontend/dist, served at /
```

- **Controllers** use `@controller(router)` from `src/api/controller.py`, with the mediator as a shared class-level dependency.
- **`build_mediator()`** in `src/infrastructure/dependency_injection.py` is the one place that wires handlers to implementations.
- **Cropping** runs on a bounded thread pool (one worker per CPU) so a heavy image never blocks the event loop.
- **Raster images** go through Pillow and NumPy; **SVGs** are rendered with resvg only to measure their content, then the `viewBox` is tightened and the markup kept.
- **The frontend** is Preact with Lucide icons. FastAPI serves it with a SPA fallback: unknown paths return `index.html`, unknown `/api` paths still return JSON 404s.
