import uuid
import datetime

from .db_layer import DBRepo
from .schemas import CategoryEnum, TransactionInputSchema, TransactionUpdateSchema


class ValidationRepo:
    """Class for user input validation"""

    def get_valid_balance_input(self) -> int:
        """Prompts user for a valid balance input."""
        while True:
            balance = input(
                "Whats your starting balance? (Should be a valid integer): "
            )
            try:
                balance = int(balance)
                return balance
            except ValueError:
                print("\nBalance should be a valid integer. Please try again.\n")

    def get_valid_amount_input(self, required: bool = True) -> int | None:
        """Prompts user for a valid amount input."""
        while True:
            amount_input = input("\nEnter the amount (A positive number): ")
            if not required and amount_input == "":
                return None

            try:
                amount = int(amount_input)
                if amount <= 0:
                    raise ValueError
                return amount
            except ValueError:
                print("\nAmount should be a positive number. Please try again.")

    def get_valid_date_input(self, required: bool = True) -> datetime.date | None:
        """Prompts user for a valid date input."""
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
                print("\nInvalid date format. Please try again.\n")

    def get_valid_category_input(self, required: bool = True) -> CategoryEnum | None:
        """Prompts user for a valid category input."""
        while True:
            category_input = input("Enter the category (expenses|incomes): ")
            if not required and category_input == "":
                return None
            try:
                category = CategoryEnum[category_input.lower()]
                return category
            except KeyError:
                print("\nInvalid category. Please try again.\n")

    def get_valid_id_input(self, db_repo: DBRepo) -> uuid.UUID | None:
        """Prompts user for a valid id input."""
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
                print("\nInvalid id format. Please try again.")

    def get_transaction_from_input(
        self, required: bool = True
    ) -> TransactionInputSchema | TransactionUpdateSchema | None:
        """Builds a transaction based on the user's input and returns it"""
        Schema = TransactionInputSchema if required else TransactionUpdateSchema

        amount = self.get_valid_amount_input(required=required)
        category = self.get_valid_category_input(required=required)
        date = self.get_valid_date_input(required=required)
        description = input("Enter description (Or leave blank): ")

        transaction = Schema(
            Amount=amount,
            Category=category,
            Date=date,
            Description=description,
        )

        return transaction
