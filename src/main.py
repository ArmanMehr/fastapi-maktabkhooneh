from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi_swagger import patch_fastapi

from schemas import ExpenseCreateModel, ExpenseResponseModel, ExpenseUpdateModel

expenses_db = [
    {"id": 0, "amount": 1000, "description": "expense-1"},
    {"id": 1, "amount": 1000, "description": "expense-2"},
    {"id": 2, "amount": 1000, "description": "expense-3"},
]
last_id = len(expenses_db) - 1

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app)


@app.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseResponseModel],
)
async def get_all_expenses():
    return expenses_db


@app.get(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseModel,
)
async def get_expense(expense_id: int = Path(ge=0)):
    for exp in expenses_db:
        if exp["id"] == expense_id:
            return exp
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {expense_id} not found.",
    )


@app.post(
    "/expenses", status_code=status.HTTP_201_CREATED, response_model=ExpenseCreateModel
)
async def create_expense(amount: int = Query(gt=0), description: str | None = None):
    global last_id
    new_id = last_id + 1

    description_str = description if description is not None else ""
    new_expense = {"id": new_id, "amount": amount, "description": description_str}
    expenses_db.append(new_expense)

    last_id += 1
    return new_expense


@app.put(
    "/expenses/{expense_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseUpdateModel,
)
async def update_expense(
    expense_id: int = Path(ge=0),
    amount: int = Query(gt=0),
    description: str | None = None,
):
    for exp in expenses_db:
        print(exp["id"])
        if exp["id"] == expense_id:
            exp["amount"] = amount
            exp["description"] = description
            return exp
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {expense_id} not found.",
    )


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int = Path(ge=0)):
    for exp in expenses_db:
        if exp["id"] == expense_id:
            expenses_db.remove(exp)
            return ""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {expense_id} not found.",
    )
