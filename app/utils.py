import json


def load_data(filename: str) -> dict:
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    return data


def save_data(filename: str, data: dict) -> None:
    with open(filename, "w") as file:
        json.dump(data, file)


def restore_db(filename: str) -> None:
    save_data(filename, {})
