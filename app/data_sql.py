import os
import sqlite3
from .models import Item
import datetime as dt

# файл має знаходитися в кореневому каталозі пакета
DATA_BASE = os.path.join(os.path.dirname(__file__), "items.db")

def read_all_items() -> list[Item]:
    with sqlite3.connect(DATA_BASE) as con:
        cursor = con.cursor()
        cursor.execute("SELECT id, message, sign, datetime FROM items")
        rows = cursor.fetchall()
        
    items = [Item(id=i, message=m, sign=s, datetime=d) for i, m, s, d in rows]
    return items

def add_item(message: str, sign: str):
   
    datetime=dt.datetime.now().isoformat()
    
    with sqlite3.connect(DATA_BASE) as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO items (message, sign, datetime) VALUES (?,?,?)",
            (message, sign, datetime) )


def do_test_db():
    """Виготовлення тестових даних"""
    with sqlite3.connect(DATA_BASE) as con:
        cursor = con.cursor()

        # створюємо таблицю items
        cursor.execute("""CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            message TEXT, 
            sign TEXT, 
            datetime TEXT)""")

        # додаємо рядки до таблиці
        for sign in ("AAA", "BBB", "CCC"):
            cursor.execute("INSERT INTO items (message, sign, datetime) VALUES (?,?,?)",
                (sign*4, sign, "2025-07-18") )
