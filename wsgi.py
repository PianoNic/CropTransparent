from waitress import serve
from src.app import app

if __name__ == "__main__":
    print("Starting Transparent Image Cropper app on http://0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)