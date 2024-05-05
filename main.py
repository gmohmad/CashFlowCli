from app.core.cash_flow import CashFlowCli


def main() -> None:
    """Greats the user and starts the app"""
    print(
        "Hello! Welcome to CashFlow, here you can manage your finances. Best of luck!\n"
    )
    app = CashFlowCli()
    app.run()


if __name__ == "__main__":
    main()
