from config.options import OPTIONS
from .db_layer import DBRepo
from .input_validation import ValidationRepo


class ServiceRepo:
    def __init__(self):
        self.validation_repo = ValidationRepo()
        self.db_repo = DBRepo(self.validation_repo.get_valid_balance_input())

    def _print_transactions(self, transactions: dict):
        print()

        if not transactions:
            print("Nothing found.\n")
            return

        for id, fields in transactions.items():
            print(f"Id: {id}")
            for field, value in fields.items():
                print(f"{field}: {value}")
            print()

    def print_options(self):
        print("Here are possible options:\n")
        for key, value in OPTIONS.items():
            print(f"{value} -- {key}")
        print()

    def show_balance(self):
        print(f"\nHere's your current balance: {self.db_repo.get_balance()}\n")

    def show_incomes(self):
        self._print_transactions(self.db_repo.get_incomes())

    def show_expenses(self):
        self._print_transactions(self.db_repo.get_expenses())

    def add_new_transaction(self):
        transaction = self.validation_repo.get_transaction_from_input()
        if transaction is None:
            print()
            return

        self.db_repo.create_transaction(transaction)

        print("\nTransaction was successfully created!\n")

    def update_transaction(self):
        id = self.validation_repo.get_valid_id_input(self.db_repo)
        if id is None:
            print()
            return
        transaction = self.validation_repo.get_transaction_from_input(required=False)

        self.db_repo.update_transaction(id, transaction)

        print("\nTransaction was successfully updated!\n")

    def find_transactions(self):
        pattern = input(
            "Enter date, amount or category of transactions you want to find: "
        )

        queryset = self.db_repo.filter_transactions(pattern)

        if not queryset:
            print("\nNo matches!\n")
            return

        self._print_transactions(queryset)