from typing import Dict
from fastapi import APIRouter, Request
from ..data_alch import read_all_probs

router = APIRouter()

@router.get("/probs")
async def get_probs(request: Request):
    probs = read_all_probs()
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

