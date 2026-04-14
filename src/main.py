from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_swagger import patch_fastapi

from exceptions import ExpenseNotFoundError
from locales.loader import translate
from routes.expenses import expenses_router
from routes.users import users_router

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
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
