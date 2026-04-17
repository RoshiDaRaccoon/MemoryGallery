from fastapi import APIRouter, Depends, HTTPException, status, Path, UploadFile, File, Form, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
import service
from typing import Optional, List, Any, Dict
from datetime import datetime, timezone
import uuid
import json
from schemas import PhotoCreateRequest, PhotoCreateResponse, PhotoReadRequest, PhotoReadResponse, PhotoUpdateRequest, PhotoUpdateResponse, PhotoDeleteRequest, PhotoDeleteResponse, ErrorResponse
from auth_utils import bearer_scheme, decode_token


photos_router = APIRouter(prefix="/photos", tags=["Photos"])

@photos_router.post("/",
        response_model=PhotoCreateResponse,
        tags=["Photos"],
        summary="Загрузить фото",
        description="Загрузка фото в систему")
async def upload_photo(photo_data_json: str = Form(...), file: UploadFile = File(...), session: AsyncSession = Depends(get_session), credentials = Depends(bearer_scheme)):
    # FastAPI не любит, когда ему передают одновременно и файл, и много параметров, поэтому все параметры загоняются в JSON на клиенте перед отправкой запроса
    # Парсим этот JSON обратно в модель для валидации
    photo_data_dict = json.loads(photo_data_json)
    photo_data = PhotoCreateRequest(**photo_data_dict)

    token = credentials.credentials
    payload = decode_token(token, token_type="access")
    user_email = payload["sub"]

    photo_service = service.PhotoService()
    return await photo_service.upload_photo(photo_data, user_email=user_email, file=file, session=session)

@photos_router.get("/",
        response_model=list[PhotoReadResponse], 
        tags=["Photos"], 
        summary="Получить все фото", 
        description="Возвращает список всех фото с использованием пагинации")
async def get_photos(limit: int = Query(20, ge=1, le=100),
                     offset: int = Query(0, ge=0),
                     grade: Optional[int] = Query(None),
                     parallel: Optional[str] = Query(None),
                     search: Optional[str] = Query(None),
                     date_from: Optional[datetime] = Query(None),
                     date_to: Optional[datetime] = Query(None),
                     session: AsyncSession = Depends(get_session)):
    photo_service = service.PhotoService()
    return await photo_service.get_all_photos(session, limit, offset, grade, parallel, search, date_from, date_to)

@photos_router.get("/{photo_id}",
        response_model=PhotoReadResponse,
        tags=["Photos"], 
        summary="Получить фото по ID", 
        description="Возвращает данные фото по его ID",
        responses={
            404: {"model": ErrorResponse, "description": "Фото не найдено"}
        })
async def get_photo(photo_id: int = Path(..., title="ID фото", description="Уникальный идентификатор фото"), session: AsyncSession = Depends(get_session)):
    photo_service = service.PhotoService()
    return await photo_service.get_photo_by_id(photo_id, session=session)

@photos_router.put("/{photo_id}",
        response_model=PhotoUpdateResponse,
        tags=["Photos"], 
        summary="Обновить фото", 
        description="Обновляет данные существующего фото",
        responses={
            404: {"model": ErrorResponse, "description": "Фото не найдено"}
        })
async def update_photo(photo_data: PhotoUpdateRequest, 
                    photo_id: int = Path(...,  title="ID фото",
                                        description="Уникальный идентификатор фото"), session: AsyncSession = Depends(get_session), credentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_token(token, token_type="access")
    user_email = payload["sub"]

    photo_service = service.PhotoService()
    return await photo_service.update_photo(photo_id, photo_data, user_email=user_email, session=session)

@photos_router.delete("/{photo_id}",
            response_model=PhotoDeleteResponse,
            tags=["Photos"], 
            summary="Удалить фото", 
            description="Удаляет фото из системы по его ID",
            responses={
                404: {"model": ErrorResponse, "description": "Фото не найдено"}
            })
async def delete_photo(photo_id: int = Path(...,  title="ID фото",
                                        description="Уникальный идентификатор фото"), session: AsyncSession = Depends(get_session), credentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_token(token, token_type="access")
    user_email = payload["sub"]

    photo_service = service.PhotoService()
    photo = await photo_service.get_photo_by_id(photo_id, session=session)
    return await photo_service.delete_photo(photo_id, photo.path, user_email=user_email, session=session)