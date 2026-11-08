import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine
from routers import router

app = FastAPI(title="IdeaBox API", version="1.0.0")
origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173,https://ideabox-5pw.pages.dev/"
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.api_route('/', methods = ["GET", "HEAD"])
async def greet():
    return({"IdeaBox":"Active"})

@app.api_route("/health", methods = ["GET", "HEAD"])
async def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return({"status": "ok", "IdeaBox": "active", "Database" : "Connected"})
    except Exception:
        return({"status": "error", "IdeaBox": "active", "Database" : "Not connected"})