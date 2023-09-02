import os
tmp_path = os.getcwd().split("Diginamic_mongo_project")[0]
target_path = os.path.join(tmp_path, 'Diginamic_mongo_project')
import sys
sys.path[:0] = [target_path]
from dotenv import load_dotenv
from scripts.models.mongo_db_singleton import MongoDBSingleton

# Titres des colonnes du dataset
ALL_COLL= ['HeartDisease', 'Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking',
               'Sex', 'AgeCategory', 'Race', 'Diabetic', 'PhysicalActivity',
               'GenHealth', 'Asthma', 'KidneyDisease', 'SkinCancer','BMI', 'PhysicalHealth', 'MentalHealth', 'SleepTime'] 

# Titre des colonnes numériques
NUM_COLUMNS = ['BMI', 'PhysicalHealth', 'MentalHealth', 'SleepTime']

# Titres des colonnes catégorielles
CAT_COLUMNS = ['HeartDisease', 'Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking',
               'Sex', 'AgeCategory', 'Race', 'Diabetic', 'PhysicalActivity',
               'GenHealth', 'Asthma', 'KidneyDisease', 'SkinCancer']

# Dictionnaire de substitution d'un nom de colonne par une expression plus humaine
COLNAMES_DICT = {'HeartDisease': "Heart disease", 'Smoking': "Smoking", 
                 'AlcoholDrinking': "Alcohol drinking", 'Stroke': "Stroke", 
                 'DiffWalking': "Walking difficulty", 'Sex': "Sex", 
                 'AgeCategory': "Age category", 'Race': "Ethnicity", 'Diabetic': "Diabetic", 
                 'PhysicalActivity': "Physical activity", 'GenHealth': "General health", 
                 'Asthma': "Asthma", 'KidneyDisease': "Kidney disease", 'SkinCancer': "Skin cancer",
                 'BMI':'BMI', 'PhysicalHealth':'Physical health', 'MentalHealth':'Mental health', 'SleepTime':'Sleep time'}

# Chemin d'accès au dataset et aux fichiers émis par l'appli
ASSETS_PATH = os.path.join(target_path, "assets")


def graph_query_generator(patient_data: dict):
    """
    A partir d'un filtre sur un certain profil patient, génère la requête propre aux graphes
    """
    data_zero = {}
    for k in patient_data.keys():
        data_zero[k] = 0
    return [{"$match": patient_data}, {"$project": data_zero}]

def get_patients_data(query):
    """
    Obtient les données des patients qui correspondent à la requête
    Args:
        query (dict): La requête de recherche des patients
    Retourne:
        list: Une liste contenant les données des patients
    """

    # charge les variables d'environnement à partir du fichier .env
    load_dotenv()

    # connecte à MongoDB et crée la collection
    db = MongoDBSingleton.get_instance()
    heart_coll = db.get_collection("heart")

    # recherche les patients qui correspondent à la requête
    results = heart_coll.find(query, {'_id': 0})
    # liste pour stocker les données des patients
    list_data_patients = []
    # itère sur les résultats et ajoute les données des patients à la liste
    for res in results:
        new_data = {}
        # ajoute les données des patients au dictionnaire new_data, sauf des clés utilisées dans la requête
        for key, value in res.items():
            if key not in query.keys():
                new_data[key] = value
        list_data_patients.append(new_data)
    return list_data_patients

def disease_estimate(collection, patient_data):
    """
    Effectue une agrégation sur la collection donnée et calcule le pourcentage de patients ayant HeartDisease:Yes
    Args:
        collection: La collection sur laquelle effectuer l'agrégation
        patient_data (dict): Les données du patient utilisées dans l'agrégation
    """
    pipeline = [
        {
            "$match": patient_data
        },
        {
            "$group": {
                "_id": "$HeartDisease",
                "count_diseases": {"$count": {}}
            }
        }
    ]
    # exécute le pipeline sur collection_name et renvoie les résultats
    results = collection.aggregate(pipeline)
    
    # initialise les variables yes_count et no_count
    yes_count = 0
    no_count = 0
    
    # pour chaque "doc" dans "results", vérifie si la valeur du champ _id est "Yes"
    for doc in results:
        # si la valeur est "Yes", incrémente la variable yes_count
        if doc["_id"] == "Yes":
            yes_count = doc["count_diseases"]
        # sinon, incrémente la variable no_count
        else:
            no_count = doc["count_diseases"]
            
    # calcule le nombre total de patients
    total_patients = yes_count + no_count
    
    # calcule le pourcentage de patients ayant HeartDisease:Yes
    percentage = (yes_count / total_patients) * 100
    
    # dictionnaire stocke les valeurs calculées
    result_dict = {
        "yes": yes_count,
        "no": no_count,
        "total": total_patients,
        "percentage": round(percentage, 2)
    }
    return result_dict

if __name__ == "__main__":
    # dictionnaire patient_data contient les données d'un seul patient (input)
    patient_data = {
        "BMI": 20 ,
        "Smoking": "Yes",
        "AlcoholDrinking": "No",
        "Stroke": "No",
        "PhysicalHealth": 3,
    }
    print(graph_query_generator(patient_data))
