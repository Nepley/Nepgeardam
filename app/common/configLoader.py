import json
import os

class Config():
    @classmethod
    def load(self):
        """
        Fonction permettant de charger le fichier de config

        Retourne un dictionnaire avec les données de configuration
        """

        if(os.path.exists("../config.json")):
            file = open("../config.json", "r", encoding="utf8")
            data = json.load(file)
            file.close
        
            return data
        else:
            raise Exception("Le fichier de configuration n'existe pas.")