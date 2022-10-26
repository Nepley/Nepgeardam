from fastapi import APIRouter
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from enum import Enum
import requests

from ..common.mongo import MongoDB
from ..common.auth import Authorization

router = APIRouter(
	prefix="/scheduler",
	tags=["Scheduler"],
	responses={404: {"description": "Not found"}},
)

mongodb_collection = "scheduler"
auth_key = "Secree0eectr21KKKEEE1eKy"

###############

class methodList(str, Enum):
	GET = "GET"
	POST = "POST"
	PUT = "PUT"
	DELETE = "DELETE"

class scaleList(str, Enum):
	MINUTE = "m"
	HOUR = "h"
	DAY = "d"
	MONTH = "M"
	YEAR = "y"


###############

@router.put("")
def add_action(authKey: str, url: str, interval: int, scale: scaleList, params: dict = {}, method: methodList = "GET", description: str = "", recurrent: bool = True):
	if(authKey == auth_key):
		db = MongoDB(mongodb_collection)
		next_date = update_next_date(interval, scale, datetime.now())
		id = db.add({'url': url, 'params': params, 'method': method, 'interval': interval, 'scale': scale, 'description': description, 'recurrent': recurrent, 'next_call': next_date})
		response = {"type": "OK", "message": "action added to the scheduler", "id": str(id)}
	else:
		response = {"type": "ERROR", "message": "You are not authorized to do this action"}
	
	return response

@router.post("")
def update_action(authKey: str, id: str, url: str, interval: int, scale: scaleList, params: dict = {}, method: methodList = "GET", description: str = "", recurrent: bool = True):
	if(authKey == auth_key):
		db = MongoDB(mongodb_collection)
		action = db.queryOne({"_id": ObjectId(id)})
		if(action != {}):
			if(url != action['url']):
				db.updateOne({"_id": ObjectId(id)}, 'url', url)
			
			if(interval != action['interval']):
				db.updateOne({"_id": ObjectId(id)}, 'interval', interval)

			if(scale != action['scale']):
				db.updateOne({"_id": ObjectId(id)}, 'scale', scale)
			
			if(params != action['params']):
				db.updateOne({"_id": ObjectId(id)}, 'params', params)
			
			if(method != action['method']):
				db.updateOne({"_id": ObjectId(id)}, 'method', method)

			if(description != action['description']):
				db.updateOne({"_id": ObjectId(id)}, 'description', description)
			
			if(recurrent != action['recurrent']):
				db.updateOne({"_id": ObjectId(id)}, 'recurrent', recurrent)
			
			response = {"type": "OK", "message": "Action updated"}
		else:
			response = {"type": "ERROR", "message": "Action does not exist"}
	else:
		response = {"type": "ERROR", "message": "You are not authorized to do this action"}
	
	return response

@router.get("")
def get_all_actions():
	db = MongoDB(mongodb_collection)

	actions = db.getAll()
	for action in actions:
		action['_id'] = str(action['_id'])

	return actions

@router.delete("")
def delete_action(authKey: str, id: str):
	if(authKey == auth_key):
		db = MongoDB(mongodb_collection)
		db.deleteOne({'_id': ObjectId(id)})
		response = {"type": "OK", "message": "Action deleted"}
	else:
		response = {"type": "ERROR", "message": "You are not authorized to do this action"}

	return response

@router.get("/exec")
def execute_action(id: str, manual: bool = True):
	db = MongoDB(mongodb_collection)

	action = db.queryOne({"_id": ObjectId(id)})
	if not manual:
		next_call = update_next_date(action['interval'], action['scale'], action['next_call'])

	requests.request(action['method'], action['url'])

	db.updateOne({"_id": ObjectId(id)}, 'next_call', next_call)

def update_next_date(interval: int, scale: scaleList, old_date: datetime):
	# next_date = old_date
	next_date = datetime.now()
	if(scale == "m"):
		next_date += timedelta(minutes=interval)
	elif(scale == "h"):
		next_date += timedelta(hours=interval)
	elif(scale == "d"):
		next_date += timedelta(days=interval)
	elif(scale == "M"):
		next_date += timedelta(month=interval)
	elif(scale == "y"):
		next_date += timedelta(year=interval)
	
	return next_date
