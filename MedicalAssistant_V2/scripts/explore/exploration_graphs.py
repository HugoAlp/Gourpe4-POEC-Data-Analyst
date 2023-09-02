''' Ce script génère les graphiques d'examen initial des données et les enregistre au format png. '''

''' Imports '''
import os
tmp_path = os.getcwd().split("MedicalAssistant_V2")[0]
target_path = os.path.join(tmp_path, 'MedicalAssistant_V2')
import sys
sys.path[:0] = [target_path]

import seaborn as sns
from matplotlib import pyplot as plt
from scripts.utils import NUM_COLUMNS, COLNAMES_DICT
from scripts.models import MongoDBSingleton

db = MongoDBSingleton.get_instance()

def singleGraphsGeneration(savingPath):

       ''' Extraction des clés '''
       keys = list(list(db.get_collection('heart').find({}, {"_id" : 0}).limit(1))[0].keys()) 

       ''' Génération des graphiques '''
       for parameters in keys :
              
              extractedData = list(db.get_collection('heart').find({}, {parameters : 1, '_id' : 0}))
              individualValues = [x[parameters] for x in extractedData]

              if parameters in NUM_COLUMNS :
                     numFig = plt.figure(figsize = (7, 7))

                     plot = sns.histplot(individualValues, kde = True, stat = "count", color = "indianred", alpha = 0.5)

                     plot.set(ylabel = 'Count', title = f'{COLNAMES_DICT[parameters]}')

                     if parameters == "BMI" : plot.set(xlabel = 'Index')
                     elif parameters == "SleepTime" : plot.set(xlabel = 'Hours')
                     else : plot.set(xlabel = 'Days since')

                     numFig.savefig(f'{savingPath}/{parameters}.png')
                     print(parameters, "ok")

              else :
                     catFig = plt.figure(figsize = (7, 7))

                     if parameters == "GenHealth" : plot = sns.countplot(x = individualValues, color = "cadetblue", order = ["Poor", "Fair", "Good", "Very good", "Excellent"], alpha = 0.8)
                     elif parameters ==  "Diabetic" : plot = sns.countplot(x = individualValues, color = "cadetblue", order = ["Yes", "Yes, during \n pregnancy", "No, borderline \n diabetes", "No"], alpha = 0.8)
                     elif parameters == "Race" : plot = sns.countplot(x = individualValues, color = "cadetblue", order = ["White", "Hispanic", "Black", "Asian", "American Indian \n / Alaskan Native", "Other"], alpha = 0.8)
                     elif parameters == "AgeCategory" : plot = sns.countplot(x = individualValues, color = "cadetblue", order = ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "74-79", "80 or older"], alpha = 0.8) ; plot.set_xticklabels(plot.get_xticklabels(), rotation = 45, horizontalalignment = 'right')
                     elif parameters == "Sex" : plot = sns.countplot(x = individualValues, color = "cadetblue", order = ["Female", "Male"], alpha = 0.8)
                     else : plot = sns.countplot(x = individualValues, color = "cadetblue", order = ["Yes", "No"], alpha = 0.8)
                     
                     plot.set(ylabel = 'Count', title = f'{COLNAMES_DICT[parameters]}')

                     catFig.savefig(f'{savingPath}/{parameters}.png')
                     print(parameters, "ok")
                     
if __name__ == '__main__':
       singleGraphsGeneration('img/')


