import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/app-info", tags=["App Info"])
def app_info():
    environment = os.environ.get('FLASK_ENV', 'unknown environment')
    version = os.environ.get('APP_VERSION', 'unknown version')
    return {"environment": environment, "version": version}