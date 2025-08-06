from typing import Dict
from fastapi import APIRouter, Request

from .. import data_alch as db
from ..models.models import PostProof, PostCheck
from ..executors import js

import re

router = APIRouter()


@router.post("/check")
async def post_check(schema: PostCheck) -> str:
    """
    Знаходить задачу, замінює авторське вирішення користувацьким,
    викликає post_proof()
    """
    problem = db.read_prob(schema.id)
    regex = regex_helper(problem.lang);
    if regex == None:
       return "Wrong Language" 
    newCode = re.sub(regex, schema.solving, problem.code, count=1, flags=re.DOTALL)
    return exec_helper(problem.lang, newCode, timeout=2)
     

@router.post("/proof")
async def post_proof(schema: PostProof) -> str:
    """
    Виконує програму, повертає повідомлення про результат.
    Повідомлення про позитивний результат починається з OK
    """
    return exec_helper(schema.lang, schema.source, timeout=2)
    
         
def regex_helper(lang:str):
    if lang == 'js':
        return r"//BEGIN.*//END"
    return None


def exec_helper(lang:str, source: str, timeout: float):
    if lang == 'js':
        return js.exec(source, timeout=timeout)
    return "Error: Unknown language"
    

@router.get("/probs")
async def get_probs(request: Request):
    probs = db.read_all_probs()
    return probs


# @router.post("/items")
# async def post_items(request: Request):
#     form = await request.form()

#     message = form.get("message").strip()
#     sign = form.get("sign").strip()
    
#     if message != '':    
#         add_item(message, sign)

#     items = read_all_items()
#     return templates.TemplateResponse("items.html", {"request": request, "items": items})


# @router.get("/freq")
# async def get_freq(request: Request):
#     items = read_all_items()
#     dict = {}
#     for item in items:
#         n: int = dict.get(item.sign, 0)
#         dict[item.sign] = n + 1
    
#     return templates.TemplateResponse("freq.html", {"request": request, "dict": dict})

