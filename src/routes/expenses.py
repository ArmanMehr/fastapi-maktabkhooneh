from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from auth import get_authenticated_user
from database import get_db
from exceptions import ExpenseNotFoundError
from locales.loader import get_language
from models import Expense, User
from schemas import (
    ExpenseCreateSchema,
    ExpenseResponseSchema,
    ExpenseUpdateSchema,
)

expenses_router = APIRouter(tags=["expenses"])


@expenses_router.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseResponseSchema],
)
async def get_all_expenses(
    user: User = Depends(get_authenticated_user), db: Session = Depends(get_db)
):
    try:
        return db.query(Expense).filter(Expense.user_id == user.id).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)


@expenses_router.get(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseSchema,
)
async def get_expense(
    expense_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
    _=Depends(get_language),
):
    query = (
        db.query(Expense)
        .filter(Expense.user_id == user.id, Expense.id == expense_id)
        .one_or_none()
    )
    if query:
        return query
    raise ExpenseNotFoundError(expense_id)


@expenses_router.post(
    "/expenses",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseResponseSchema,
)
async def create_expense(
    request: ExpenseCreateSchema,
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
    _=Depends(get_language),
):
    new_expense = Expense(**request.model_dump(), user_id=user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@expenses_router.put(
    "/expenses/{expense_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseResponseSchema,
)
async def update_expense(
    expense_id: int,
    request: ExpenseUpdateSchema,
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
    _=Depends(get_language),
):
    expense = (
        db.query(Expense)
        .filter(Expense.user_id == user.id, Expense.id == expense_id)
        .one_or_none()
    )
    if not expense:
        raise ExpenseNotFoundError(expense_id)

    for field in request.model_dump().keys():
        setattr(expense, field, getattr(request, field))
    db.commit()
    db.refresh(expense)
    return expense


@expenses_router.delete(
    "/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_expense(
    expense_id: int = Path(gt=0),
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
    _=Depends(get_language),
):
    expense = (
        db.query(Expense)
        .filter(Expense.user_id == user.id, Expense.id == expense_id)
        .one_or_none()
    )
    if not expense:
        raise ExpenseNotFoundError(expense_id)

    db.delete(expense)
    db.commit()
