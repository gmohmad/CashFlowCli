import uuid
from .utils import load_data, save_data, restore_db
from .schemas import (
    TransactionSchema,
    TransactionInputSchema,
    TransactionUpdateSchema,
    CategoryEnum,
)


DB_PATH = "db/db.json"


class DBRepo:
    def __init__(self, balance: int) -> None:
        restore_db(DB_PATH)
        self.BALANCE = balance
        self.data = load_data(DB_PATH)

    def update_balance(self, category: CategoryEnum, amount: int) -> None:
        if category == CategoryEnum.incomes:
            self.BALANCE += amount
        else:
            self.BALANCE -= amount

    def restore_balance(self, category: CategoryEnum, amount: int) -> None:
        if category == CategoryEnum.incomes:
            self.BALANCE -= amount
        else:
            self.BALANCE += amount

    def get_balance(self):
        return self.BALANCE

    def get_incomes(self) -> dict[uuid.UUID, TransactionSchema]:
        return {
            k: v for k, v in self.data.items() if v["Category"] == CategoryEnum.incomes
        }

    def get_expenses(self) -> dict[uuid.UUID, TransactionSchema]:
        return {
            k: v for k, v in self.data.items() if v["Category"] == CategoryEnum.expenses
        }

    def get_transaction_by_id(self, id: uuid.UUID) -> TransactionSchema | None:
        return self.data.get(str(id))

    def filter_transactions(self, pattern: str) -> dict[uuid.UUID, TransactionSchema]:
        return {
            k: v
            for k, v in self.data.items()
            if v["Category"].lower() == pattern.lower()
            or str(v["Amount"]) == pattern
            or v["Date"] == pattern
        }

    def create_transaction(self, data: TransactionInputSchema):
        id = str(uuid.uuid4())
        self.data[id] = data.model_dump()
        save_data(DB_PATH, self.data)

        self.update_balance(data.Category, data.Amount)

    def update_transaction(
        self, id: uuid.UUID, new_data: TransactionUpdateSchema
    ) -> TransactionSchema | None:
        transaction = self.get_transaction_by_id(id)

        if transaction is None:
            raise LookupError("A transaction with this id does not exist")

        if new_data.Amount:
            self.restore_balance(transaction["Category"], transaction["Amount"])
            self.update_balance(
                new_data.Category or transaction["Category"], new_data.Amount
            )

        for k, v in new_data.model_dump().items():
            if v is not None:
                transaction[k] = v

        self.data[str(id)] = transaction

        save_data(DB_PATH, self.data)

        return transaction
