from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth import decode_verify_refresh_token, generate_jwt_token
from configs import get_settings
from database import get_db
from locales.loader import get_language, translate
from models import User
from schemas import UserLoginSchema, UserRegisterSchema
from utils import hash_password, verify_password

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegisterSchema,
    db: Session = Depends(get_db),
    lang=Depends(get_language),
):
    if db.query(User).filter(User.username == request.username).one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=translate(lang=lang, msgid="username_exists"),
        )
    password_hashed = hash_password(request.password)
    new_user = User(username=request.username, password=password_hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(
        content={"detail": translate(lang=lang, msgid="user_register_success")}
    )


@users_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    request: UserLoginSchema,
    response: Response,
    db: Session = Depends(get_db),
    lang=Depends(get_language),
):
    user = db.query(User).filter(User.username == request.username).one_or_none()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang=lang, msgid="incorrect_uname_pass"),
        )

    refresh_token = generate_jwt_token(type="refresh", user_id=user.id)
    access_token = generate_jwt_token(type="access", user_id=user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=get_settings().JWT_ACCESS_TOKEN_DUR,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=get_settings().JWT_REFRESH_TOKEN_DUR,
    )

    return JSONResponse(
        content={"detail": translate(lang=lang, msgid="login_success")},
        headers=response.headers,
    )


@users_router.post("/refresh", status_code=status.HTTP_200_OK)
async def user_refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    lang=Depends(get_language),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang=lang, msgid="refresh_token_not_found"),
        )

    user_id = decode_verify_refresh_token(refresh_token)
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang=lang, msgid="failed_auth_unauthorized_user"),
        )

    new_token = generate_jwt_token(type="access", user_id=user.id)
    response.set_cookie(
        key="access_token",
        value=new_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=get_settings().JWT_ACCESS_TOKEN_DUR,
    )
    return JSONResponse(
        content={"detail": translate(lang=lang, msgid="token_gen_success")},
        headers=response.headers,
    )


@users_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
