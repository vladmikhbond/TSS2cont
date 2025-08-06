import json, os
from .models.models import Item
from datetime import datetime

# файл має знаходитися в кореневому каталозі пакета
DATA_FILE = os.path.join(os.path.dirname(__file__), "items.json")

def read_all_items() -> list[Item]:
    with open(DATA_FILE, "r") as f:
        return [Item(**item) for item in json.load(f)]

                  
def write_all(items: list[Item]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump([item.__dict__ for item in items], f, ensure_ascii=False, indent=4)


def add_item(message: str, sign: str) -> None:
    item = Item(
        message=message.strip(), 
        sign=sign.strip(), 
        datetime=datetime.now().isoformat())
    items = read_all_items()
    items.append(item)
    write_all(items)


def do_test_db() -> None:
    """Виготовлення тестових даних"""
    items = [Item(message=s*4, sign=s, datetime="2025-07-11") for s in ["aaa", "bbb", "ccc"]]
    write_all(items)
