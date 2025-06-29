import fastapi, uvicorn
from fastapi import FastAPI
import dotenv, os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "Aviation API"
VERSION = "0.1.0"
DEBUG_MODE = os.getenv("DEBUG MODE", "True").lower() == "true"
app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    debug=DEBUG_MODE
)