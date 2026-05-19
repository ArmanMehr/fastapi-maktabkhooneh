from datetime import datetime, timedelta, timezone
from logging import getLogger
from typing import Any, Literal, Optional

from fastapi import Depends, HTTPException, Request, status
from jwt import ExpiredSignatureError, PyJWTError, decode, encode
from sqlalchemy.orm import Session

from configs import get_settings
from database import get_db
from locales.loader import get_language, translate
from models import User

JWT_ALGORITHM = "HS256"

logger = getLogger(__name__)


def generate_jwt_token(type: Literal["access", "refresh"], user_id: int) -> str:
    now = datetime.now(timezone.utc)
    exp_seconds = (
        get_settings().JWT_ACCESS_TOKEN_DUR
        if type == "access"
        else get_settings().JWT_REFRESH_TOKEN_DUR
    )

    payload = {
        "type": type,
        "user_id": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=exp_seconds)).timestamp()),
    }

    return encode(payload, key=get_settings().JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_check_jwt_token(
    token: str, expected_type: str = "access", lang: str = "en"
) -> dict[str, Any]:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang, "authentication_required"),
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        decoded = decode(
            token,
            key=get_settings().JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": True},
        )

        required = ["type", "user_id", "exp"]
        for item in required:
            if item not in decoded:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=translate(lang, "invalid_token_structure"),
                )

        if decoded.get("type") != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=translate(lang, "invalid_token_type"),
            )

        return decoded

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang, "token_expired"),
            headers={"X-Token-Expired": "true"},
        )

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=translate(lang, "invalid_token"),
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unexpected error in token validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=translate(lang, "internal_error"),
        )


def decode_verify_refresh_token(token: str, lang: str = "en") -> int:
    decoded = decode_check_jwt_token(token, expected_type="refresh", lang=lang)

    if decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang, "invalid_refresh_token"),
        )

    return decoded["user_id"]


def get_authenticated_user(
    request: Request,
    db: Session = Depends(get_db),
    lang: str = Depends(get_language),
) -> Optional[User]:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang, "authentication_required"),
            headers={"WWW-Authenticate": "Bearer"},
        )

    decoded = decode_check_jwt_token(token, expected_type="access", lang=lang)

    user_id = decoded.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang, "invalid_token_structure"),
        )

    user = db.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang, "user_not_found"),
        )

    return user
