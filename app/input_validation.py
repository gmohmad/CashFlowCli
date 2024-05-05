import uuid
import datetime

from .db_layer import DBRepo
from .schemas import CategoryEnum, TransactionInputSchema, TransactionUpdateSchema


class ValidationRepo:

    def get_valid_balance_input(self) -> int:
        while True:
            balance = input(
                "Whats your starting balance? (Enter a non-negative number) "
            )
            try:
                balance = int(balance)
                if balance < 0:
                    raise ValueError
                return balance
            except ValueError:
                print("\nBalance should be a non-negative number. Please try again.\n")

    def get_valid_amount_input(self, required: bool = True) -> int | None:
        """Prompt the user for a valid amount input."""
        while True:
            amount_input = input("\nEnter the amount (A positive number|Cancel -- c): ")
            if amount_input == "c":
                return None

            if not required and amount_input == "":
                return None
            try:
                amount = int(amount_input)
                if amount <= 0:
                    raise ValueError
                return amount
            except ValueError:
                print("Amount should be a positive number. Please try again.\n")

    def get_valid_date_input(self, required: bool = True) -> datetime.date | None:
        """Prompt the user for a valid date input."""
        while True:
            date_input = input("Enter the date (YYYY-MM-DD) or type 't' to autofill: ")
            if not required and date_input == "":
                return None
            if date_input == "t":
                date = datetime.datetime.now()
                return datetime.date(date.year, date.month, date.day)
            try:
                date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
                return date
            except ValueError:
                print("Invalid date format. Please try again.\n")

    def get_valid_category_input(self, required: bool = True) -> str | None:
        """Prompt the user for a valid category input."""
        while True:
            category_input = input("Enter the category (expenses|incomes): ")
            if not required and category_input == "":
                return None
            try:
                category = CategoryEnum[category_input.lower()]
                return category.value
            except KeyError:
                print("Invalid category. Please try again.\n")

    def get_valid_id_input(self, db_repo: DBRepo) -> uuid.UUID | None:
        """Prompt the user for a valid id input."""
        while True:
            try:
                id_input = input(
                    "\nEnter the id of the transation you want to update (Cancel -- c): "
                )
                if id_input == "c":
                    return None

                id = uuid.UUID(id_input)
                if not db_repo.get_transaction_by_id(id):
                    print("A transaction with this id was not found. Please try again.")
                    continue

                return id
            except ValueError:
                print("\nInvalid id format. Please try again.\n")

    def get_transaction_from_input(
        self, required: bool = True
    ) -> TransactionInputSchema | TransactionUpdateSchema | None:
        """"""
        Schema = TransactionInputSchema if required else TransactionUpdateSchema

        if required:
            amount = self.get_valid_amount_input()
            if amount is None:
                return None
            category = self.get_valid_category_input()
            date = self.get_valid_date_input()

        if not required:
            amount = self.get_valid_amount_input(required=False)
            category = self.get_valid_category_input(required=False)
            date = self.get_valid_date_input(required=False)

        description = input("Enter description (Or leave blank): ")

        transaction = Schema(
            Amount=amount,
            Category=category,
            Date=date,
            Description=description,
        )

        return transaction
