import uuid
from enum import Enum
from datetime import date
from pydantic import BaseModel, field_serializer


class CategoryEnum(str, Enum):
    """Enum for transaction category field"""

    incomes = "Incomes"
    expenses = "Expenses"


class BaseTransactionSchema(BaseModel):
    """Base transaction schema"""

    @field_serializer("Date", check_fields=False)
    def serialize_date(self, date: date) -> str:
        """Converts date to a string"""
        return str(date)


class BaseInputOutputTransactionSchema(BaseTransactionSchema):
    """Base schema for transaction input/output"""

    Amount: int
    Description: str | None = None
    Date: date
    Category: CategoryEnum


class TransactionSchema(BaseInputOutputTransactionSchema):
    """Schema for transaction data output"""

    Id: uuid.UUID


class TransactionInputSchema(BaseInputOutputTransactionSchema):
    """Schema for transaction data input"""

    pass


class TransactionUpdateSchema(BaseTransactionSchema):
    """Schema for transaction data update"""

    Amount: int | None = None
    Description: str | None = None
    Date: date | None = None
    Category: CategoryEnum | None = None
