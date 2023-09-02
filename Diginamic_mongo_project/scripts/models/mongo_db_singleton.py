from pymongo import MongoClient
import os
from dotenv import load_dotenv

# charge les variables d'environnement à partir du fichier .env
load_dotenv()
# lit les variables d'environnement comme ceci : os.environ.get('KEY_THAT_MIGHT_EXIST', default_value)

# class représente un singleton utilisé pour se connecter à MongoDB
class MongoDBSingleton:
    __instance = None
  
    @staticmethod
    def get_instance():
        """
        Retourne l'instance de `MongoDBSingleton`
        Si l'instance n'existe pas, elle en crée une nouvelle
        """
        if MongoDBSingleton.__instance is None:
            MongoDBSingleton()
        return MongoDBSingleton.__instance

    def __init__(self):
        """
        Le constructeur de la classe `MongoDBSingleton`
        Lève une exception si l'instance a déjà été créée
        """
        if MongoDBSingleton.__instance is not None:
            raise Exception("Ce Singleton est déjà instancié ! Utilisez la méthode get_instance().")
        else:
            MongoDBSingleton.__instance = self
            # connecte au serveur MongoDB
            self.client = MongoClient(os.environ.get('MONGO_HOST', 'localhost'), int(os.environ.get('MONGO_PORT', 27017)))
            # sélectionne la base de données
            self.db = self.client[os.environ.get('MONGO_DB_NAME')]

    def __collection_exists(self, collection_name: str):
        """
        Vérifie si une collection existe dans la base de données
        Args :
            collection_name (str) : Le nom de la collection à vérifier
        Retourne :
            True si la collection existe, False sinon
        """        
        if collection_name in self.db.list_collection_names():
            return True
        return False

    def get_collection(self, collection_name: str):
        """
        Retourne la collection avec le nom donné
        Args :
            collection_name (str) : Le nom de la collection à renvoyer
        Retourne :
            La collection portant le nom donné
        """
        if self.__collection_exists(collection_name):
            return self.db[collection_name]
        else:
            print("La collection", collection_name, "n'existe pas !")

    def add_to_collection(self, collection_name: str, data: dict):
        """
        Ajoute un document à la collection avec le nom donné
        Args : 
            collection_name (str) : Le nom de la collection à laquelle ajouter le document
            data (dict) : Le document à ajouter
        """
        if self.__collection_exists(collection_name):
            self.db[collection_name].insert_one(data)
            print("Ajout terminé.")
        else:
            print("La collection", collection_name, "n'existe pas !")

    def create_collection(self, collection_name:str, validator=None):
        """
        Crée une nouvelle collection avec le nom donné
        Args :
            collection_name (str) : Le nom de la collection à créer
            validator (dict) : Le validateur de la collection
        """
        if self.__collection_exists(collection_name):
            print("Une vue ou collection", collection_name, "existe déjà !")
        else:
            self.db.create_collection(collection_name)
            if validator:
                self.db.command({'collMod': collection_name, 'validator': validator})
            print("Collection créée.")

    def generate_view(self, view_name, target_collection_name: str, pipeline: list):
        """
        Génère une vue si elle n'existe pas déjà
        Si elle existe déjà, affiche un message d'erreur
        Args :
            view_name (str): Le nom de la vue à générer
            target_collection_name (str): Le nom de la collection cible de la vue
            pipeline (list): Le pipeline de la vue
        """
        if self.__collection_exists(view_name):
            print("Une vue ou collection", view_name, "existe déjà !")        
        else:
            self.db.command({"create": view_name, "viewOn": target_collection_name, "pipeline": pipeline })
            print("Vue créée.")

    def drop_collection(self, collection_name:str):
        """
        Supprime une vue ou collection en fonction de son nom
        Args:
        collection_name (str): Le nom de la vue ou collection à supprimer
        """
        if collection_name == "heart":
            print("Attention ! 'heart' est la collection principale et ne peut être supprimée.")
        elif self.__collection_exists(collection_name):
            self.db[collection_name].drop()
            print("Vue ou collection supprimée.")
        else:
            print("Aucune vue ou collection", collection_name, "n'a été trouvée !")

