from pydantic import BaseModel, Field, StrictInt, field_validator

from models import Expense


class ExpenseBaseShema(BaseModel):
    amount: int = Field(..., gt=0)
    description: str = Field(default="", max_length=250)


class ExpenseResponseSchema(ExpenseBaseShema):
    id: StrictInt = Field(..., gt=0)

    @classmethod
    def validate_from_expense(
        cls, expense: Expense
    ) -> "ExpenseResponseSchema":
        return cls(
            id=expense.id,
            amount=expense.amount,
            description=expense.description or "",
        )


class ExpenseCreateSchema(ExpenseBaseShema):
    pass


class ExpenseUpdateSchema(ExpenseBaseShema):
    pass


class UserRegisterSchema(BaseModel):
    username: str = Field(..., max_length=250)
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)

    @classmethod
    @field_validator("password_confirm", mode="after")
    def check_password_confirm(cls, password_confirm):
        if not password_confirm == cls.password:
            raise ValueError("Password confirm doesn't match with password")
        return password_confirm


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=250)
    password: str = Field(..., min_length=8)


class UserRefreshTokenSchema(BaseModel):
    token: str
