import string
import random
from .mongo import MongoDB

mongodb_collection = "Authorization_list"

class Authorization():
    @classmethod
    def add(self, id_col: str, name: str = "") -> str:
        """Add a new key link to an id

        Args:
            id (str): Id to link the key
            name (str, optional): Name to describe the key. Defaults to "".

        Returns:
            str: The new generated key linked to the id
        """
        key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(15))

        mdb = MongoDB(mongodb_collection)

        mdb.add({'id_col': id_col, 'name': name, 'key': key})

        return key
    
    @classmethod
    def delete(self, id: str, key: str):
        """Delete a key

        Args:
            id (str): id linked to the key
            key (str): key to delete
        """
        mdb = MongoDB(mongodb_collection)
        mdb.deleteOne({'id': id, 'key': key})

    @classmethod
    def isAuthorized(self, id_col: str, key: str) -> bool:
        """Check if the key is a good key linked to the Id

        Args:
            id_col (str): Id to test
            key (str): Key to test

        Returns:
            bool: True if they are linked, False if not
        """
        mdb = MongoDB(mongodb_collection)
        result = mdb.queryOne({'id_col': id_col, 'key': key})
        return True if result != None else False