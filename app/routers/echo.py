from fastapi import APIRouter
from bson.objectid import ObjectId
from pydantic import BaseModel

from ..common.collection import Collection
from ..common.auth import Authorization

router = APIRouter(
    prefix="/echo",
    tags=["Echo"],
    responses={404: {"description": "Not found"}},
)

mongodb_collection = "echo"

#####Models######

class standardResponse(BaseModel):
    status: str
    message: str

class createCollQuote(BaseModel):
    id: str
    authKey: str

class echoResponse(BaseModel):
    id: str
    echo: str

#################

@router.get("", response_model=echoResponse)
def get_echo(id: str, tag: str):
    echoCollection = Collection(mongodb_collection, id)

    echo = echoCollection.getOne({"tag": tag})

    if echo != None:
        return {'id': str(echo["_id"]), 'echo': echo['echo']}
    else:
        return {'id': '', 'echo': ''}

@router.get("/list")
def get_list_tag(id: str):
    echoCollection = Collection(mongodb_collection, id)

    echoes = echoCollection.getAll()

    list_tag = []
    for echo in echoes:
        list_tag.append({'id': str(echo['_id']),'tag': echo['tag']})

    return list_tag

@router.put("", response_model=standardResponse)
def add_echo(echo: str, tag: str, id: str, authKey: str):
    echoCollection = Collection(mongodb_collection, id)
    
    msg = echoCollection.add({'echo': echo, 'tag': tag}, authKey)
    if msg['status'] == 'OK':
        return {"status": "OK", "message": "Echo added"}
    else:
        return {"status": "ERROR", "message": "Error while adding the echo: "+msg['message']}

@router.delete("", response_model=standardResponse)
def delete_echo(id: str, id_echo: str, authKey: str):
    echoCollection = Collection(mongodb_collection, id)

    msg = echoCollection.delete({"_id": ObjectId(id_echo)}, authKey)
    if msg['status'] == 'OK':
        return {'status': 'OK', 'message': 'Echo deleted'}
    else:
        return {"status": "ERROR", "message": "Error while deleting the echo: "+msg['message']}

@router.put('/create', response_model=createCollQuote)
def create_collection_echo():
    infos = Collection.create(mongodb_collection)
    return infos