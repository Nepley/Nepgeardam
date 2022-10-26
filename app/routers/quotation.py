from typing import List
from fastapi import APIRouter
from bson.objectid import ObjectId
import random
from datetime import datetime
from pydantic import BaseModel

from ..common.collection import Collection
from ..common.auth import Authorization

router = APIRouter(
    prefix="/quote",
    tags=["Quote"],
    responses={404: {"description": "Not found"}},
)

mongodb_collection = "quote"

#####Models######

class randomQuote(BaseModel):
    id: str
    quote: str
    author: str
    date: str

class standardResponse(BaseModel):
    status: str
    message: str

class statQuote(BaseModel):
    stats: dict
    Total: int

class createCollQuote(BaseModel):
    id: str
    authKey: str

class allQuote(BaseModel):
    id: str
    author: str
    quote_list: list

#################

@router.get("", response_model=randomQuote)
def get_random_quote(id: str, author: str = ""):
    quotes = Collection(mongodb_collection, id)

    listQuote = []
    if(author == ""):
        listQuote = quotes.getAll()
    else:
        listQuote = quotes.get({"author": author})

    quote = random.choice(listQuote)

    return {"id": str(quote['_id']), "quote": quote['quote'], "author": quote['author'], 'date':quote['date']}

@router.put("", response_model=standardResponse)
def add_quote(quote: str, author: str, id: str, authKey: str, date: str = ""):
    quotes = Collection(mongodb_collection, id)
    if(date == ""):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")

    msg = quotes.add({'quote': quote, 'author': author, 'date': date}, authKey)
    if msg['status'] == 'OK':
        return {"status": "OK", "message": "Quote added"}
    else:
        return {"status": "ERROR", "message": "Error while adding the quote: "+msg['message']}

@router.get("/all", response_model=allQuote)
def get_all_quote(id: str, author: str = ""):
    quotes = Collection(mongodb_collection, id)

    listQuote = []
    if(author == ""):
        listQuote = quotes.getAll()
    else:
        listQuote = quotes.get({"author": author})

    for quote in listQuote:
        quote['id'] = str(quote['_id'])
        quote.pop('_id', None)

    return {"id": id, "author": author, "quote_list": listQuote}

@router.get("/stats", response_model=statQuote)
def get_stats(id: str):
    quoteCollection = Collection(mongodb_collection, id)
    quotes = quoteCollection.getAll()
    stats = {}

    for quote in quotes:
        stats[quote['author']] = stats[quote['author']]+1 if quote['author'] in stats else 1
    
    # Sort
    stats ={k: v for k, v in sorted(stats.items(), key=lambda item: item[1], reverse=True)}

    return {'stats': stats, 'Total': len(quotes)}

@router.delete("", response_model=standardResponse)
def delete_quote(id: str, id_quote: str, authKey: str):
    quoteCollection = Collection(mongodb_collection, id)

    msg = quoteCollection.delete({"_id": ObjectId(id_quote)}, authKey)
    if msg['status'] == 'OK':
        return {'status': 'OK', 'message': 'Quote deleted'}
    else:
        return {"status": "ERROR", "message": "Error while deleting the quote: "+msg['message']}

@router.put('/create', response_model=createCollQuote)
def create_collection_quote():
    infos = Collection.create(mongodb_collection)
    return infos