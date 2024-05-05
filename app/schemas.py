import uuid
from enum import Enum
from datetime import date
from pydantic import BaseModel, field_serializer


class CategoryEnum(str, Enum):
    incomes = "Incomes"
    expenses = "Expenses"


class BaseTransactionSchema(BaseModel):

    @field_serializer("Date", check_fields=False)
    def serialize_date(self, date: date):
        return str(date)


class BaseInputOutputTransactionSchema(BaseTransactionSchema):
    Amount: int
    Description: str | None = None
    Date: date
    Category: CategoryEnum


class TransactionSchema(BaseInputOutputTransactionSchema):
    Id: uuid.UUID


class TransactionInputSchema(BaseInputOutputTransactionSchema):
    pass


class TransactionUpdateSchema(BaseTransactionSchema):
    Amount: int | None = None
    Description: str | None = None
    Date: date | None = None
    Category: CategoryEnum | None = None
