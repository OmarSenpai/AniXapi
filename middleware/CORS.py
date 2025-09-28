from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import app

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

