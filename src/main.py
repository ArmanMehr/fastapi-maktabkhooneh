from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse

expenses_db = [
    {"id": 0, "amount": 1000, "description": "expense-1"},
    {"id": 1, "amount": 1000, "description": "expense-2"},
    {"id": 2, "amount": 1000, "description": "expense-3"},
]
last_id = 2

app = FastAPI()


@app.get("/expenses")
async def get_all_expenses() -> JSONResponse:
    return JSONResponse(content=expenses_db, status_code=status.HTTP_200_OK)


@app.get("/expenses/{expense_id}")
async def get_expense(expense_id: int = Path(ge=0)) -> JSONResponse:
    for exp in expenses_db:
        if exp["id"] == expense_id:
            return JSONResponse(content=exp, status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {expense_id} not found.",
    )


@app.post("/expenses")
async def create_expense(
    amount: int = Query(gt=0), description: str | None = None
) -> JSONResponse:
    global last_id
    new_id = last_id + 1

    description_str = description if description is not None else ""
    new_expense = {"id": new_id, "amount": amount, "description": description_str}
    expenses_db.append(new_expense)

    last_id += 1
    return JSONResponse(content=new_expense, status_code=status.HTTP_201_CREATED)


@app.put("/expenses/{expense_id}")
async def update_expense(
    expense_id: int = Path(ge=0),
    amount: int = Query(gt=0),
    description: str | None = None,
) -> JSONResponse:
    for exp in expenses_db:
        print(exp["id"])
        if exp["id"] == expense_id:
            exp["amount"] = amount
            exp["description"] = description
            return JSONResponse(content=exp, status_code=status.HTTP_201_CREATED)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {expense_id} not found.",
    )


@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int = Path(ge=0)) -> JSONResponse:
    for exp in expenses_db:
        if exp["id"] == expense_id:
            expenses_db.remove(exp)
            return JSONResponse(content="", status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {expense_id} not found.",
    )
