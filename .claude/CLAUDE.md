# CropTransparent Claude workflow rules

Never push to `main`. Every change goes:

1. **Issue**: open one (or pick existing) with at least one label from `gh label list`.
2. **Branch**: `feature/<issue#>_PascalCase` for new / refactor / docs, `fix/<issue#>_PascalCase` for bugs.
3. **PR**: short imperative title; body is one-line summary + `Closes #<issue>`; at least one label.
4. **Squash-merge + delete branch**, then `git fetch --prune && git reset --hard origin/main`.

## Branch naming

- ✅ `feature/18_SvgSupportAndOnionArchitecture`
- ✅ `fix/16_ReverseProxyPaths`

## PR body

One line in commit-subject style, then `Closes #<issue>`. The commits already say what changed, so the PR doesn't need to repeat them.

```
Implemented animated GIF cropping

Closes #9
```

## Commit subject

Past tense, verb first, short: about 3–7 words, one idea, no body. No "and … and …" lists, no file paths. Squash merges end with `(#PR)`.

- `Added <thing>`
- `Fixed <thing>`
- `Rebuilt <thing>`
- `Removed <thing>`

Examples:

- `Rebuilt the frontend in Preact (#21)`
- `Fixed server overload from upload floods (#23)`
- `Guarded the log handler against duplicates`

Release bumps (written by `release.yaml`): `Bumped application.properties to X for release [skip ci]`.

No AI attribution of any kind: no `Co-Authored-By:` trailers (Claude, Copilot or otherwise) and no "Generated with Claude Code" footers. Squash-merge with `--body ""` so GitHub doesn't append trailers from the PR's commits.

## Labels

Pick from `gh label list`. CropTransparent's active set: `feature`, `enhancement`, `bug`, `refactor`. Release Drafter resolves the next version from them (`feature`/`enhancement` → minor, `bug`/`refactor` → patch, `breaking` → major).

## Project

FastAPI backend (onion architecture, CQRS via mediatorx) that crops transparent edges, flat backgrounds and SVG viewBoxes; Preact frontend in `frontend/` served by FastAPI as a SPA.

- **Run**: `cd frontend && npm install && npm run build`, then `python asgi.py` (http://localhost:5000). Python 3.11+.
- **Frontend dev**: `npm run dev` in `frontend/`; Vite proxies `/api` to port 5000.
- **Tests**: `python -m pytest tests`.
- **Docker**: `docker compose up` (multi-stage build: Node builds the SPA, Python serves it).
- **Version**: `application.properties` (`APP_VERSION`, `APP_ENVIRONMENT`). Don't bump it by hand; publishing a release runs `.github/workflows/release.yaml`, which writes the tag into it on main and then builds the image.
- **Icons**: Lucide (`lucide-preact`). The knife illustration is `frontend/src/Cutter.jsx`.
