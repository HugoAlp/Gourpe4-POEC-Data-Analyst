# ce fichier contient le code d'installation de votre application (doit être exécuté en premier et une seule fois)
from scripts.models.mongo_db_singleton import MongoDBSingleton
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd

load_dotenv()

# connexion à la base et création des collections
db = MongoDBSingleton.get_instance()

# récupération des données
data = pd.read_csv("assets/heart_2020_cleaned.csv")

# passage des floats à int
for titre_col in data.select_dtypes('float64').columns:
    data[titre_col] = data[titre_col].round().astype(int)

# construction du validateur
validator = {'$jsonSchema': {'required': ['HeartDisease'], 'properties': {}}}
for titre_col in data.select_dtypes('int32').columns:
    validator['$jsonSchema']['properties'][titre_col] = {"bsonType": "int"}
for titre_col in data.select_dtypes('object').columns:
    validator['$jsonSchema']['properties'][titre_col] = {"bsonType": "string"}

# création de la collection
db.create_collection("heart", validator)

# insertion des données en base, avec affichage d'une barre de progression
with tqdm(total=len(data)) as pbar:
    for v in tqdm(data.iterrows()):
        db.add_to_collection("heart", v[1].to_dict())
        pbar.update()


