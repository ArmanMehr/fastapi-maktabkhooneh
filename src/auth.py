from datetime import datetime, timedelta, timezone
from typing import Any, Literal, Optional

from fastapi import Depends, HTTPException, Request, status
from jwt import decode, encode
from sqlalchemy.orm import Session

from configs import get_settings
from database import get_db
from locales.loader import get_language, translate
from models import User

JWT_ALGORITHM = "HS256"


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


def decode_check_jwt_token(token: str, lang=Depends(get_language)) -> dict[str, Any]:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang=lang, msgid="failed_auth_missing_token"),
        )

    try:
        decoded = decode(
            token,
            key=get_settings().JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        required = ["type", "user_id", "exp"]
        for item in required:
            if item not in decoded:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=translate(
                        lang=lang, msgid="failed_auth_missing_element_intoken"
                    ),
                )

        if datetime.now(timezone.utc) > datetime.fromtimestamp(
            decoded["exp"], tz=timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=translate(lang=lang, msgid="failed_auth_token_exp"),
            )

        return decoded

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed, {e}",
        )


def decode_verify_refresh_token(token: str, lang=Depends(get_language)) -> int:
    decoded = decode_check_jwt_token(token)

    if decoded["type"] != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang=lang, msgid="failed_auth_invalid_ref_token"),
        )

    return decoded["user_id"]


def get_authenticated_user(
    request: Request, db: Session = Depends(get_db), lang=Depends(get_language)
) -> Optional[User]:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(lang=lang, msgid="failed_auth_invalid_access_token"),
        )
    try:
        decoded = decode_check_jwt_token(token)

        if decoded.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=translate(lang=lang, msgid="failed_auth_invalid_access_token"),
            )

        user_id = decoded.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=translate(lang=lang, msgid="failed_auth_not_found_userid"),
            )

        user = db.query(User).filter(User.id == user_id).one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=translate(lang=lang, msgid="failed_auth_user_not_found"),
            )

        return user

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed. An unexpected error occurred: {e}",
        )
