from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi_swagger import patch_fastapi
from sqlalchemy.orm import Session

from database import Expense, get_db
from schemas import ExpenseCreateModel, ExpenseResponseModel, ExpenseUpdateModel

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app)


@app.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseResponseModel],
)
async def get_all_expenses(db: Session = Depends(get_db)):
    try:
        return db.query(Expense).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)


@app.get(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseModel,
)
async def get_expense(expense_id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    if query:
        return query
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {expense_id} not found.",
    )


@app.post(
    "/expenses",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseCreateModel,
)
async def create_expense(
    amount: int = Query(gt=0),
    description: str | None = None,
    db: Session = Depends(get_db),
):
    description_str = description if description is not None else ""
    new_expense = Expense(amount=amount, description=description_str)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@app.put(
    "/expenses/{expense_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseUpdateModel,
)
async def update_expense(
    expense_id: int = Path(gt=0),
    amount: int = Query(gt=0),
    description: str | None = None,
    db: Session = Depends(get_db),
):
    expense = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found.",
        )
    expense.amount = amount
    expense.description = description
    db.commit()
    db.refresh(expense)
    return expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int = Path(gt=0), db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found.",
        )
    db.delete(expense)
    db.commit()
    db.refresh(expense)
