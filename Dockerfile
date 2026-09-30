FROM node:24-alpine AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.13.5-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY asgi.py application.properties ./
COPY src/ src/
COPY --from=frontend /frontend/dist frontend/dist

EXPOSE 5000

CMD ["python", "asgi.py"]
