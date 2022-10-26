from pymongo import MongoClient
from typing import Union
import json

# Global parameters for MongoDB
mongodb_ip = "mongodb"
mongodb_port = 27017
mongodb_db = "NepgeardamMkIII"

class MongoDB():
    def __init__(self, collection: str):
        """Create a connecton with a collection from MongoDB

        Args:
            collection (str): Name of the collection
        """
        # Connecting to MongoDB
        self.__client = MongoClient(mongodb_ip, mongodb_port)

        # We retrieve the database
        self.__database = self.__client[mongodb_db]

        self.__collection = self.__database[collection]

    def add(self, data: Union[str, dict]) -> str:
        """Add a new value to the collection

        Args:
            data (Union[str, dict]): Data to add

        Raises:
            Exception: Exception raise if the data is not valid

        Returns:
            str: Id of inserted element
        """
        if(not isinstance(data, dict)):
            # Check if it's a valid JSON / Converting it to a dict
            try:
                data = json.loads(data)
            except Exception as e:
                raise Exception("The data provided is not a valid JSON")

        insert =  self.__collection.insert_one(data)
        return insert.inserted_id

    def addMany(self, datas: list) -> list:
        """Add mutliple elements to the collection

        Args:
            datas (list): List of data to add

        Returns:
            list: Id list of the elements added
        """
        inserts = self.__collection.insert_many(datas)
        return inserts.inserted_ids

    def getAll(self) -> list:
        """Get all element from the collection

        Returns:
            list: Elements from the collection
        """
        elements = self.__collection.find()
        # Converting to a list
        element_list = []
        for element in elements:
            element_list.append(element)
        return element_list

    def query(self, filter: dict, fields: list = []) -> list:
        """Search for an element of the collection

        Args:
            filter (dict): Filter of the search
            fields (list, optional): List of field to get. Defaults to [].

        Returns:
            list: Elements found by the query
        """
        if fields != []:
            field = {}
            for f in fields:
                field[f] = 1
            elements = self.__collection.find(filter, field)
        else:
            elements = self.__collection.find(filter)
        # Converting to a list
        element_list = []
        for element in elements:
            element_list.append(element)
        return element_list

    def queryOne(self, filter: dict, fields: list = []) -> dict:
        """search one element from the collection

        Args:
            filter (dict): Filter of the search
            fields (list, optional): List of field to get. Defaults to [].

        Returns:
            dict: Element found by the query
        """
        if fields != []:
            field = {}
            for f in fields:
                field[f] = 1
            element = self.__collection.find_one(filter, field)
        else:
            element = self.__collection.find_one(filter)

        return element

    def deleteOne(self, filter: dict):
        """Delete one element from the collection

        Args:
            filter (dict): Filter of the search
        """
        self.__collection.delete_one(filter)

    def delete(self, filter: dict) -> int:
        """Delete multiple elements from the collection

        Args:
            filter (dict): Filter of the search

        Returns:
            int: Number of element deleted
        """
        deleted = self.__collection.delete_many(filter)
        return deleted.deleted_count

    def updateOne(self, filter: dict, field: str, newValue: Union[str, int]):
        """Update one element from the collection

        Args:
            filter (dict): Filter of the search
            field (str): Field to update
            newValue (Union[str, int]): New value of the field
        """
        value = {"$set": {field: newValue}}
        self.__collection.update_one(filter, value)

    def update(self, filter: dict, field: str, newValue: Union[str, int]) -> int:
        """Update multiple elements from the collection

        Args:
            filter (dict): Filter of the search
            field (str): Field to update
            newValue (Union[str, int]): New value of the field

        Returns:
            int: Number of element updated
        """
        value = {"$set": {field: newValue}}
        updated = self.__collection.update_many(filter, value)
        return updated.modified_count

    def drop(self):
        """Drop the collection
        """
        self.__collection.drop()