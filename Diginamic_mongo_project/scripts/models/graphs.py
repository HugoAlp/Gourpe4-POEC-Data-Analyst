import os
tmp_path = os.getcwd().split("Diginamic_mongo_project")[0]
target_path = os.path.join(tmp_path, 'Diginamic_mongo_project')
import sys
sys.path[:0] = [target_path]

def batchGraphsGeneration(dataPatient,savingPath) :

    ''' Imports '''
    import seaborn as sns
    from matplotlib import pyplot as plt
    from scripts.utils import CAT_COLUMNS, NUM_COLUMNS, graph_query_generator
    import pandas as pd
    import math
    from scripts.models.mongo_db_singleton import MongoDBSingleton
    
    db = MongoDBSingleton.get_instance()

    ''' Création d'une vue '''
    
    db.generate_view(view_name = "newView", target_collection_name = "heart", pipeline = graph_query_generator(dataPatient))

    ''' Importation '''

    df = pd.DataFrame(list(db.get_collection("newView").find({}, {"_id" : 0})))

    ''' Traitement des variables catégorielles '''

    catFig = plt.figure(figsize = (32, 32))
    catFig.suptitle('Categorial Parameters', fontsize = 30)

    for i in range(0, len(CAT_COLUMNS)):

        axs = catFig.add_subplot(4, 4, i + 1)

        axs.set_title(label = f'{CAT_COLUMNS[i]}', fontsize = 20)
        axs.set_ylabel("Count", fontsize = 20)

        if CAT_COLUMNS[i] in df.columns :

            index = list(df.columns).index(CAT_COLUMNS[i])

            if CAT_COLUMNS[i] == "GenHealth" : 
                plot = sns.countplot(ax = axs, x = df.iloc[:, index], color = "cadetblue", order = ["Poor", "Fair", "Good", "Very good", "Excellent"], alpha = 0.8)
                plot.set(xlabel = '')
            elif CAT_COLUMNS[i] ==  "Diabetic" :
                plot = sns.countplot(ax = axs, x = df.iloc[:, index], color = "cadetblue", order = ["Yes", "Yes, during \n pregnancy", "No, borderline \n diabetes", "No"], alpha = 0.8)
                plot.set(xlabel = '')
            elif CAT_COLUMNS[i] == "Race" :
                plot = sns.countplot(ax = axs, x = df.iloc[:, index], color = "cadetblue", order = ["White", "Hispanic", "Black", "Asian", "American Indian \n / Alaskan Native", "Other"], alpha = 0.8)
                plot.set(xlabel = '')
            else : 
                plot = sns.countplot(ax = axs, x = df.iloc[:, index], color = "cadetblue", order = ["Yes", "No"], alpha = 0.8)
                plot.set(xlabel = '')
                
    plt.show()        
    # catFig.savefig(f'{savingPath}/catFig.png')

    ''' Traitement des variables numériques '''

    numFig = plt.figure(figsize = (32, 8))
    numFig.suptitle('Numerical Parameters', fontsize = 30)

    for i in range(0, len(NUM_COLUMNS)):

        axs = numFig.add_subplot(1, 4, i + 1)

        axs.set_title(label = f'{NUM_COLUMNS[i]}', fontsize = 20)
        axs.set_ylabel("Count", fontsize = 20)

        if NUM_COLUMNS[i] in df.columns :

            index = list(df.columns).index(NUM_COLUMNS[i])
            plot = sns.histplot(ax = axs, x = df.iloc[:, index], kde = True, stat = "count", color = "indianred", alpha = 0.5)
            plot.set(xlabel = '')
            if NUM_COLUMNS[i] == "BMI" : plot.set(xlabel = 'Index')
            elif NUM_COLUMNS[i] == "SleepTime" : plot.set(xlabel = 'Hours')
            else : plot.set(xlabel = 'Days since')

    plt.show()
    # numFig.savefig(f'{savingPath}/numFig.png')

    ''' Drop la vue '''
