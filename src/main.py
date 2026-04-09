from fastapi import FastAPI
from fastapi_swagger import patch_fastapi

from routes.expenses import expenses_router
from routes.users import users_router

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app)

app.include_router(users_router)
app.include_router(expenses_router)
