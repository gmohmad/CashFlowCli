import uuid
from .utils.db_utils import load_data, save_data
from .schemas import (
    TransactionSchema,
    TransactionInputSchema,
    TransactionUpdateSchema,
    CategoryEnum,
)


DB_PATH: str = "db/db.json"


class DBRepo:
    """Class for db operations"""

    def __init__(self, balance: int) -> None:
        """Set up balance and db data"""
        self.BALANCE = balance
        self.data = load_data(DB_PATH)

    def update_balance(self, category: CategoryEnum, amount: int) -> None:
        """Updates balance based on the category"""
        if category == CategoryEnum.incomes:
            self.BALANCE += amount
        else:
            self.BALANCE -= amount

    def restore_balance(self, category: CategoryEnum, amount: int) -> None:
        """Restores balance based on the category"""
        if category == CategoryEnum.incomes:
            self.BALANCE -= amount
        else:
            self.BALANCE += amount

    def get_balance(self) -> int:
        "Returns the balance"
        return self.BALANCE

    def get_incomes(self) -> dict[uuid.UUID, TransactionSchema]:
        """Returns a dict containing incomes"""
        return {
            k: v for k, v in self.data.items() if v["Category"] == CategoryEnum.incomes
        }

    def get_expenses(self) -> dict[uuid.UUID, TransactionSchema]:
        """Returns a dict containing expenses"""
        return {
            k: v for k, v in self.data.items() if v["Category"] == CategoryEnum.expenses
        }

    def get_transaction_by_id(self, id: uuid.UUID) -> TransactionSchema | None:
        """Returns a transaction by id or none if one with given id does not exist"""
        return self.data.get(str(id))

    def filter_transactions(self, pattern: str) -> dict[uuid.UUID, TransactionSchema]:
        """Returns a dict containing transactions that satisfy the query pattern"""
        return {
            k: v
            for k, v in self.data.items()
            if v["Category"].lower() == pattern.lower()
            or str(v["Amount"]) == pattern
            or v["Date"] == pattern
        }

    def create_transaction(self, data: TransactionInputSchema) -> None:
        """Adds a new transaction to db and updates balance"""
        id = str(uuid.uuid4())
        self.data[id] = data.model_dump()
        save_data(DB_PATH, self.data)

        self.update_balance(data.Category, data.Amount)

    def update_transaction(
        self, id: uuid.UUID, new_data: TransactionUpdateSchema
    ) -> TransactionSchema | None:
        """Updates transaction with given id and updates balance if it exists"""
        transaction = self.get_transaction_by_id(id)

        if new_data.Amount:
            self.restore_balance(transaction["Category"], transaction["Amount"])
            self.update_balance(
                new_data.Category or transaction["Category"], new_data.Amount
            )
        elif new_data.Category:
            self.restore_balance(transaction["Category"], transaction["Amount"])
            self.update_balance(new_data.Category, transaction["Amount"])

        for k, v in new_data.model_dump().items():
            if v is not None:
                transaction[k] = v

        self.data[str(id)] = transaction

        save_data(DB_PATH, self.data)

        return transaction
