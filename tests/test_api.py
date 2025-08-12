from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Problem

client = TestClient(app)

def test_get_problems_lang():
    response = client.get("/api/problems/lang/js")
    assert response.status_code == 200
    assert len(response.json()) > 280
    
def test_get_problems_id():
    response = client.get("/api/problems/4b1aa936-9d3c-40a8-b4c8-154c2d2ccecd")
    assert response.status_code == 200
    assert response.json()['attr'] == "js/01 Числа та вирази"
    
def test_post_check():
    body = {
        "id": "4b1aa936-9d3c-40a8-b4c8-154c2d2ccecd",      
        "solving": "let sec = 366 * 24 * 60 * 60"
    }
    response = client.post("/api/check", json=body)    
    assert response.status_code == 200
    assert response.json() == "OK"
    
def test_post_problems():
    body = {
        "title": "TEST TEST TEST TEST TEST TEST TEST TEST Скільки секунд",
        "attr": "js/01 Числа та вирази",
        "lang": "js",
        "cond": "Напишіть програму, яка підрахує, скільки секунд у 2024 році.\r\nРезультат збережіть у змінній sec.\r\n",
        "view": "let sec = ",
        "hint": "//BEGIN\r\nlet sec = \r\n//END",
        "code": "//BEGIN\r\nlet sec = 366 * 24 * 60 * 60\r\n//END\r\nif (sec != 366 * 24 * 60 * 60) \r\n   throw new Error('Wrong');\r\nthrow new Error('OK');",
        "author": "opr"
    }
    response = client.post("/api/problems", json=body)    
    assert response.status_code == 200
    assert len(response.text) == 38         # 38 = length of uuid + 2
    
def test_put_problems():
    body = {
        "id": "4b1aa936-9d3c-40a8-b4c8-154c2d2ccecd",
        "title": "TEST TEST TEST TEST TEST TEST TEST TEST Скільки секунд",
        "attr": "js/01 Числа та вирази",
        "lang": "js",
        "cond": "Напишіть програму, яка підрахує, скільки секунд у 2024 році.\r\nРезультат збережіть у змінній sec.\r\n",
        "view": "let sec = ",
        "hint": "//BEGIN\r\nlet sec = \r\n//END",
        "code": "//BEGIN\r\nlet sec = 366 * 24 * 60 * 60\r\n//END\r\nif (sec != 366 * 24 * 60 * 60) \r\n   throw new Error('Wrong');\r\nthrow new Error('OK');",
        "author": "opr"
    }
    response = client.put("/api/problems", json=body)    
    assert response.status_code == 200
    assert response.text == '"4b1aa936-9d3c-40a8-b4c8-154c2d2ccecd"'

from app.data_alch import add_problem
    
def test_delete_problems_id():
    body = {
        "title": "TEST TEST TEST TEST TEST TEST TEST TEST Скільки секунд",
        "attr": "js/01 Числа та вирази",
        "lang": "js",
        "cond": "Напишіть програму, яка підрахує, скільки секунд у 2024 році.\r\nРезультат збережіть у змінній sec.\r\n",
        "view": "let sec = ",
        "hint": "//BEGIN\r\nlet sec = \r\n//END",
        "code": "//BEGIN\r\nlet sec = 366 * 24 * 60 * 60\r\n//END\r\nif (sec != 366 * 24 * 60 * 60) \r\n   throw new Error('Wrong');\r\nthrow new Error('OK');",
        "author": "opr"
    }
    problem = add_problem(Problem(**body))
    if problem is None: 
        return False

    response = client.delete("/api/problems/" + problem.id)    
    assert response.status_code == 200
    assert response.json()['attr'] == "js/01 Числа та вирази"
