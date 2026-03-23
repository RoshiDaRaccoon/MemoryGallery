from contextlib import asynccontextmanager
import os
from typing import List
from fastapi import FastAPI, Path, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import service as service_module
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_db, get_db_session
import schemas as schemas
from routers.users_routes import users_router
from routers.auth_routes import router as auth_router
from routers.photos_routes import photos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="MemoryGallery API",
    description="API для сервиса MemoryGallery",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.swagger_ui_parameters = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": "your-client-id",
}

photos_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "photos")
if not os.path.exists(photos_dir_path):
    os.makedirs(photos_dir_path, exist_ok=True)
app.mount("/public-photos", StaticFiles(directory=photos_dir_path), name="public_photos")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(photos_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["./"],
        reload_delay=0.25
    ) 