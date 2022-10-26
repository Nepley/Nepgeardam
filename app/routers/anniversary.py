from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from bson.objectid import ObjectId

from ..common.collection import Collection
from ..common.auth import Authorization
from .misc import get_random_booru_image

router = APIRouter(
    prefix="/anniversary",
    tags=["Anniversary"],
    responses={404: {"description": "Not found"}},
)

mongodb_collection = "anniversary"

#####Models######

class standardResponse(BaseModel):
    status: str
    message: str

class createColl(BaseModel):
    id: str
    authKey: str

#################

@router.put("", response_model=standardResponse)
def add_anniversary(id: str, authKey: str, name: str, day: int, month: int, tag_1: str = "", tag_2: str = ""):
    anniversaries = Collection(mongodb_collection, id)

    msg = anniversaries.add({"name": name, "day": day, "month": month, "tag_1": tag_1, "tag_2": tag_2}, authKey)

    if msg['status'] == 'OK':
        return {"status": "OK", "message": "Anniversary added"}
    else:
        return {"status": "ERROR", "message": "Error while adding the anniversary: "+msg['message']}

@router.delete("", response_model=standardResponse)
def delete_anniversary(id: str, authKey: str, id_anniversary: str):
    anniversaries = Collection(mongodb_collection, id)

    msg = anniversaries.delete({"_id": ObjectId(id_anniversary)}, authKey)

    if msg['status'] == 'OK':
        return {'status': 'OK', 'message': 'Anniversary deleted'}
    else:
        return {"status": "ERROR", "message": "Error while deleting the anniversary: "+msg['message']}

@router.get("/getAll")
def get_all_anniversary(id: str):
    anniversaryCollection = Collection(mongodb_collection, id)
    anniversaries = []
    for anniversary in anniversaryCollection.getAll():
        anniversaries.append({'id': str(anniversary['_id']), 'name': anniversary['name'], 'day': anniversary['day'], 'month': anniversary['month'], 'tag_1': anniversary['tag_1'], 'tag_2': anniversary['tag_2']})
    return anniversaries

@router.get("")
def get_today_anniversary(id: str):
    anniversaryCollection = Collection(mongodb_collection, id)

    anniversaries = anniversaryCollection.getAll()
    now = datetime.now()

    today_anniv = []
    for anniversary in anniversaries:
        if anniversary['day'] == now.day and anniversary['month'] == now.month:
            if(anniversary['tag_1'] != ""):
                image = get_random_booru_image(anniversary['tag_1'], anniversary['tag_2'])
            else:
                image = {}
            today_anniv.append({'id': str(anniversary['_id']), 'name': anniversary['name'], 'image': image})
    
    return today_anniv


@router.put('/create', response_model=createColl)
def create_collection_anniversary():
    infos = Collection.create(mongodb_collection)
    return infos