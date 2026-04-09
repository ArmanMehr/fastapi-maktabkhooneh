from pydantic import BaseModel, Field, StrictInt


class ExpenseBaseModel(BaseModel):
    amount: int = Field(..., gt=0)
    description: str = Field(default="", max_length=50)


class ExpenseResponseModel(ExpenseBaseModel):
    id: StrictInt = Field(..., ge=0)


class ExpenseCreateModel(ExpenseBaseModel):
    id: StrictInt = Field(..., ge=0)


class ExpenseUpdateModel(ExpenseBaseModel):
    id: StrictInt = Field(..., ge=0)
