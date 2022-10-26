from fastapi import APIRouter
import random
from pydantic import BaseModel
from typing import List
from pybooru import Danbooru

router = APIRouter(
    tags=["Miscellaneous"],
    responses={404: {"description": "Not found"}},
)

#####Models######

class diceResponse(BaseModel):
    total: int
    result: List[int]

class booruResponse(BaseModel):
    found: bool
    url: str

#################

@router.get("/dice")
def dice(dices: int, faces: int, minValue: int = 1):
    total = 0
    results = []
    for i in range(0, dices):
        result = random.randint(minValue, faces)
        total += result
        results.append(result)

    return {'total': total, 'results': results}

@router.get("/booru", response_model=booruResponse)
def get_random_booru_image(tag1: str, tag2: str = ""):
    Cl = Danbooru(site_url="https://safebooru.donmai.us")
    tag = tag1
    if(tag2 != ""):
        tag += " "+tag2
    Liste = Cl.post_list(tags=tag, random=True)

    response = {'found': False, 'url': ""}
    if(bool(Liste)):
        response = {'found': True, 'url': f"https://safebooru.donmai.us/posts/{Liste[0]['id']}"}
        
    return response
