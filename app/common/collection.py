import string
import random

from app.common.auth import Authorization
from .mongo import MongoDB

mongodb_listCollection = "collectionList"

class Collection():
	@classmethod
	def create(self, name: str) -> dict:
		"""Create a new collection. Since a collection doesn't exist until some data are added, we create an id for it and store it in a collection with a list of the existing collection

		Args:
			name (str): Prefix of the collection

		Returns:
			str: Id of the new collection
		"""
		# We create an id for the collection
		id = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(15))
		collectionName = f"{name}_{id}"

		# We add the collection to a collection listing all the collections
		mdb = MongoDB(mongodb_listCollection)

		mdb.add({'collectionName': collectionName, 'name': name, 'id': id})

		# We create a auth key for this collection
		authKey = Authorization.add(collectionName, f"Key to manage the collection {collectionName}")

		# We return the id and the authKey
		return {'id': id, 'authKey': authKey}

	def __init__(self, name: str, id: str):
		"""Manage a collection

		Args:
			name (str): prefix of the collection
			id (str): Id of the collection
		"""
		mdb = MongoDB(mongodb_listCollection)
		self.__info = mdb.queryOne({'name': name, 'id': id})

		if(self.__info != {}):
			self.__collection = MongoDB(self.__info['collectionName'])
		else:
			raise Exception("Collection doesn't exist")

	def deleteCollection(self, authKey: str):
		"""Delete a collection

		Args:
			authKey (str): Key necessary to do this action

		Raises:
			Exception: Error if not authorized to do this action
		"""
		if(Authorization.isAuthorized(self.__info['id'], authKey)):
			# Deletion from the collection of collection
			mdb = MongoDB(mongodb_listCollection)
			mdb.deleteOne({'id': self.__info['collectionName']})

			# Deletion of the collection
			self.__collection.drop()

			return {'status': 'OK', 'message': 'Collection deleted'}
		else:
			return {'status': 'ERROR', 'message': 'Not authorized to do this action'}

	def getInfo(self):
		"""Return the info of the colllection

		Returns:
			dict: Informations of the collection
		"""
		return self.__info

	def add(self, data: dict, authKey: str):
		"""Add a new entry in the collection

		Args:
			data (dict): Data to add
			authKey (str): Key necessary to do this action

		Raises:
			Exception: Error if not authorized to do this action
		"""
		if(Authorization.isAuthorized(self.__info['collectionName'], authKey)):
			self.__collection.add(data)

			return {'status': 'OK', 'message': 'data added'}
		else:
			return {'status': 'ERROR', 'message': 'Not authorized to do this action'}

	def getAll(self) -> list:
		"""Get all date of the collection

		Returns:
			dict: data of the collection
		"""
		return self.__collection.getAll()

	def get(self, filter: dict) -> list:
		"""Return entries corresponding to the filter

		Args:
			filter (dict): filter of the data

		Returns:
			list: list of data found
		"""
		return self.__collection.query(filter)

	def getOne(self, filter: dict) -> dict:
		"""Return one entry corresponding to the filter

		Args:
			filter (dict): filter of the data

		Returns:
			dict: data found
		"""
		return self.__collection.queryOne(filter)

	def delete(self, filter: dict, authKey: str) -> int:
		"""Delete entries corresponding to the filter

		Args:
			filter (dict): filter of the elements
			authKey (str): Key necessary to do this action

		Raises:
			Exception: Error if not authorized to do this action

		Returns:
			int: Number of element deleted
		"""
		if(Authorization.isAuthorized(self.__info['collectionName'], authKey)):
			delet = self.__collection.delete(filter)
			return {'status': 'OK', 'message': 'data deleted', 'Number_element': delet}
		else:
			return {'status': 'ERROR', 'message': 'Not authorized to do this action'}

	def deleteOne(self, filter: dict, authKey: str):
		"""Delete One entry corresponding to the filter

		Args:
			filter (dict): filter of the elements
			authKey (str): Key necessary to do this action

		Raises:
			Exception: Error if not authorized to do this action
		"""
		if(Authorization.isAuthorized(self.__info['collectionName'], authKey)):
			self.__collection.deleteOne(filter)

			return {'status': 'OK', 'message': 'data deleted'}
		else:
			return {'status': 'ERROR', 'message': 'Not authorized to do this action'}