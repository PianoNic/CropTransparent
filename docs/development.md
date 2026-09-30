# Development

Python 3.14 and Node 24 are what CI and the Docker image use.

## Run from source

```bash
cd frontend && npm install && npm run build && cd ..
pip install -r requirements.txt
python asgi.py
```

The app runs on <http://localhost:5000> and serves the built frontend from `frontend/dist`.

## Frontend with hot reload

```bash
python asgi.py            # backend on :5000
cd frontend && npm run dev # frontend on :5173, proxies /api to :5000
```

## Tests and linting

```bash
pip install pytest httpx ruff
python -m pytest tests
ruff check . && ruff format --check .
```

`src/api/controller.py` is vendored from fastapi-utils via SchulwareAPI and excluded from linting so it can be re-synced unchanged.

## Contributing

Every change goes through an issue, a `feature/<issue>_Name` or `fix/<issue>_Name` branch and a labelled PR that is squash-merged. The full rules live in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md).
