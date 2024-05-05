from app.service_layer import ServiceRepo


class CashFlowCli:
    def __init__(self):
        self.service_repo = ServiceRepo()

    def run(self):
        self.service_repo.print_options()

        while True:
            action = input("What do you want to do now? (Remind options - 8) ")

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
            else:
                print("\nInvalid option.\n")
