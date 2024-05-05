from app.service_layer import ServiceRepo


class CashFlowCli:
    """Class that sets everything up and runs the app"""

    def __init__(self) -> None:
        """Initialize service repo"""
        self.service_repo = ServiceRepo()

    def run(self) -> None:
        """Runs the app and processes user option input"""
        self.service_repo.print_options()

        while True:
            action = input("What do you want to do now? (Remind options - r): ")

            if action == "r":
                self.service_repo.print_options()
            elif action == "gb":
                self.service_repo.show_balance()
            elif action == "gi":
                self.service_repo.show_incomes()
            elif action == "ge":
                self.service_repo.show_expenses()
            elif action == "a":
                self.service_repo.add_new_transaction()
            elif action == "u":
                self.service_repo.update_transaction()
            elif action == "f":
                self.service_repo.find_transactions()
            elif action == "q":
                print("\nBye!\n")
                quit()
            else:
                print("\nInvalid option.\n")
