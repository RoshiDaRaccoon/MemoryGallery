from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from schemas import UserCreateRequest, UserCreateResponse, Token, TokenRefresh, CSRFToken
from service import UserService
import auth_utils

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/check-init",
        tags=["Users"],
        summary="Есть ли админы в системе",
        description="Возвращает true, если в системе есть зарегистрированные админы, и false в ином случае")
async def check_initialization(session: AsyncSession = Depends(get_session)):
    user_service = UserService()
    users = await user_service.get_all_users(session=session)
    return {"is_initialized": len(users) > 0}

@router.post("/register/first",
            response_model=Token,
            tags=["Auth"],
            summary="Регистрация первого пользователя")
async def register_first(user_data: UserCreateRequest, key: str, session: AsyncSession = Depends(get_session)):
    """Регистрация первого пользователя"""
    user_service = UserService()
    check = await user_service.get_all_users(session=session)
    if check:
        raise HTTPException(status_code=403, detail="Another admin already exists")
    elif key != auth_utils.MASTER_ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid master secret key")
    else:
        await user_service.create_user(user_data, session=session)
        access_token = auth_utils.create_access_token(user_data.email)
        refresh_token = auth_utils.create_refresh_token(user_data.email)
        # Сохраняем refresh_token в базе
        await user_service.update_user_refresh_token(user_data.email, refresh_token, session=session)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/register",
            response_model=Token,
            tags=["Auth"], 
            summary="Регистрация пользователя")
async def register(user_data: UserCreateRequest, session: AsyncSession = Depends(get_session), credentials = Depends(auth_utils.bearer_scheme)):
    """Регистрация нового пользователя от лица существующего"""

    # Получаем пользователя из access_token
    token = credentials.credentials
    payload = auth_utils.decode_token(token, token_type="access")

    user_service = UserService()
    user = await user_service.get_user_by_email(payload["sub"], session=session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    await user_service.create_user(user_data, session=session)
    # Если надо сразу получить доступ к системе
    # access_token = auth_utils.create_access_token(user_data.email)
    # refresh_token = auth_utils.create_refresh_token(user_data.email)
    # Сохраняем refresh_token в базе
    # await user_service.update_user_refresh_token(user_data.email, refresh_token, session=session)
    # return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    return {"message": f"User {user_data.email} created successfully"}

@router.post("/login",
            tags=["Auth"],
            response_model=Token,
            summary="Логин по email и паролю",
            description="В поле username указывайте email. Это ограничение OAuth2PasswordRequestForm.")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user_service = UserService()
    # username = email (по стандарту OAuth2PasswordRequestForm)
    user = await user_service.authenticate_user(form_data.username, form_data.password, session=session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = auth_utils.create_access_token(user.email)
    refresh_token = auth_utils.create_refresh_token(user.email)
    await user_service.update_user_refresh_token(user.email, refresh_token, session=session)
    # Устанавливаем Refresh Token в защищенную куку
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,   # Скрипты (JS) не смогут прочитать куку
        secure=False,    # Поставь True, когда будет HTTPS (на проде)
        samesite="lax",
        max_age=14 * 24 * 60 * 60 # 14 дней
    )
    
    # В JSON возвращаем ТОЛЬКО access_token
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh",
            tags=["Auth"])
async def refresh_token(response: Response, refresh_token: str = Cookie(None), session: AsyncSession = Depends(get_session)):
    """Обновление refresh-токена"""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    payload = auth_utils.decode_token(refresh_token, token_type="refresh")
    user_service = UserService()
    user = await user_service.get_user_by_email(payload["sub"], session=session)

    if not user or user.refresh_token != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    new_access_token = auth_utils.create_access_token(user.email)
    new_refresh_token = auth_utils.create_refresh_token(user.email)

    await user_service.update_user_refresh_token(user.email, new_refresh_token, session=session)

    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True)
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout",
            tags=["Auth"],
            summary="Выход из системы")
async def logout(response: Response, session: AsyncSession = Depends(get_session), credentials = Depends(auth_utils.bearer_scheme)):
    """Выход из системы"""
    # Получаем пользователя из access_token
    token = credentials.credentials
    payload = auth_utils.decode_token(token, token_type="access")
    user_service = UserService()
    await user_service.update_user_refresh_token(payload["sub"], None, session=session)
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}

@router.get("/csrf-token",
            response_model=CSRFToken,
            tags=["Auth"],
            summary="CSRF Token")
async def get_csrf_token():
    """Создание и получение csrf-токена"""
    csrf_token = auth_utils.create_csrf_token()
    return {"csrf_token": csrf_token}