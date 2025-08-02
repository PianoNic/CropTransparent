import uvicorn
from src.app import app

if __name__ == "__main__":
    print("Starting Transparent Image Cropper FastAPI app on http://0.0.0.0:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
