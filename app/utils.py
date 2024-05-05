import json


def load_data(filename: str) -> dict:
    """Loads data form db file"""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    return data


def save_data(filename: str, data: dict) -> None:
    """Saves data to db file"""
    with open(filename, "w") as file:
        json.dump(data, file)


def restore_db(filename: str) -> None:
    """Restores db by writing an empty dict to it"""
    save_data(filename, {})
