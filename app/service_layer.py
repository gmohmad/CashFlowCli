from config.options import OPTIONS
from .db_layer import DBRepo
from .input_validation import ValidationRepo


class ServiceRepo:
    """Service class"""

    def __init__(self) -> None:
        """Initializes repos"""
        self.validation_repo = ValidationRepo()
        self.db_repo = DBRepo(self.validation_repo.get_valid_balance_input())

    def _print_transactions(self, transactions: dict) -> None:
        """Prints transactions"""
        print()

        if not transactions:
            print("Nothing found.\n")
            return

        for id, fields in transactions.items():
            print(f"Id: {id}")
            for field, value in fields.items():
                print(f"{field}: {value}")
            print()

    def print_options(self) -> None:
        """Prints options"""
        print("Here are possible options:\n")
        for key, value in OPTIONS.items():
            print(f"{value} -- {key}")
        print()

    def show_balance(self) -> None:
        """Prints current balance"""
        print(f"\nHere's your current balance: {self.db_repo.get_balance()}\n")

    def show_incomes(self) -> None:
        """Prints incomes"""
        self._print_transactions(self.db_repo.get_incomes())

    def show_expenses(self) -> None:
        """Prints expenses"""
        self._print_transactions(self.db_repo.get_expenses())

    def add_new_transaction(self) -> None:
        """Promts user to enter data and creates a transaction based on it"""
        transaction = self.validation_repo.get_transaction_from_input()

        self.db_repo.create_transaction(transaction)

        print("\nTransaction was successfully created!\n")

    def update_transaction(self) -> None:
        """Promts user to enter data and updates the transaction based on it"""
        id = self.validation_repo.get_valid_id_input(self.db_repo)
        if id is None:
            print()
            return
        transaction = self.validation_repo.get_transaction_from_input(required=False)

        self.db_repo.update_transaction(id, transaction)

        print("\nTransaction was successfully updated!\n")

    def find_transactions(self) -> None:
        """Promts user to enter pattern and filters transactions based on it"""
        pattern = input(
            "Enter date, amount or category of transactions you want to find: "
        )

        queryset = self.db_repo.filter_transactions(pattern)

        if not queryset:
            print("\nNo matches!\n")
            return

        self._print_transactions(queryset)
