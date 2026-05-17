from contextlib import asynccontextmanager
from logging import getLogger

import sentry_sdk
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_swagger import patch_fastapi
from redis import asyncio as aioredis

from configs import get_settings
from exceptions import ExpenseNotFoundError
from locales.loader import translate
from routes.expenses import expenses_router
from routes.users import users_router

logger = getLogger(__name__)


try:
    sentry_sdk.init(dsn=get_settings().SENTRY_DSN, traces_sample_rate=1.0)
except Exception as e:
    logger.warning(f"Unable to initilize sentry: {e}")


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url(get_settings().REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    try:
        yield
    finally:
        await redis.close()
        FastAPICache.reset()


app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
    root_path="/api/v1",
)
patch_fastapi(app)

app.include_router(users_router)
app.include_router(expenses_router)


@app.exception_handler(ExpenseNotFoundError)
async def handle_expense_not_found(request: Request, exc):
    lang = request.headers.get("accept-language", "en")
    message = translate(lang=lang, msgid="expense_not_found_id")
    message += f" {exc.expense_id}"

    response_data = {
        "error": True,
        "status_code": status.HTTP_404_NOT_FOUND,
        "message": message,
    }
    return JSONResponse(
        content=response_data, status_code=status.HTTP_404_NOT_FOUND
    )


@app.get("/is-ready", status_code=status.HTTP_200_OK, include_in_schema=False)
async def readiness():
    return JSONResponse(
        content={"detail": "Service is ready!"}, status_code=status.HTTP_200_OK
    )


@app.get(
    "/sentry-debug", status_code=status.HTTP_200_OK, include_in_schema=False
)
async def trigger_error():
    div_by_zero = 1 / 0
    return div_by_zero
