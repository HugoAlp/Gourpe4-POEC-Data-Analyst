""" Imports des librairies """
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
from scripts.models import MongoDBSingleton
from scripts.utils import ALL_COLL, CAT_COLUMNS, NUM_COLUMNS
from scipy.stats import shapiro, bartlett
from tableone import TableOne


""" Accession au singleton """
tmp_path = os.getcwd().split("MedicalAssistant_V2")[0]
target_path = os.path.join(tmp_path, 'MedicalAssistant_V2')
sys.path[:0] = [target_path]

""" Création d'une instance """
db = MongoDBSingleton.get_instance()

"""
    Notes :

    - Variables catégorielles :
        On réalise un Chi2.
        Conditions d'application :
            - Au  moins 5 individus dans chaque groupe (ok).

    - Variables numériques :
        On réalise un t-test.
        Conditions d'application :
            - Indépendance des deux groupes
            - Normalité
            - Homoscédasticité
"""

""" Importation des données """
data = pd.DataFrame(list(db.get_collection("heart").find({}, {'_id' : 0})))

""" Matrice de corrélations """
df =  data[data.columns].replace({'Yes':1, 'No':0, 'Male':1,'Female':0,'No, borderline diabetes':'0','Yes (during pregnancy)':'1' })
df = df.drop(columns = ["GenHealth", "AgeCategory", "Race", "Diabetic"])

import matplotlib.pyplot as plt
import seaborn as sns
correlation = df.corr().round(2)
plt.figure(figsize = (14,7))
sns.heatmap(correlation, annot = True, cmap = 'YlOrBr')
plt.xticks(rotation=20, horizontalalignment='right')
plt.show()

""" Réalisation préliminaire des tests statistiques univariés """
mytable = TableOne(data,
                   columns = ALL_COLL,
                   categorical = [x for x in CAT_COLUMNS if x != 'HeartDisease'],
                   groupby = ['HeartDisease'],
                   pval = True)

print(mytable.tabulate(tablefmt = "fancy_grid"))
mytable.to_excel('./scripts/explore/tests_préliminaires.xlsx')

""" Variables qualitatives """
"""
    Le fichier mytable confirme que chacun des échantillons est constitué d'au moins 5 individus.
    On regroupe les classes d'âge deux à deux afin de d'étoffer les effectifs des plus petites qui comprennent
    environ 100 individus sur les 319 000 initiaux.
    On recode le reste des variables en binaire pour celles à deux classes et on les one-hot encode
    lorsqu'elles en contiennent strictement plus de deux.
"""

""" Variables quantitatives """
"""
    Indépendance des échantillons :
        - valeurs observées dans les différents groupes indépendantes les unes des autres.
"""

"""
    Normalité :
        - Vérifiée visuellement
        - Le Théorème Central Limite la suppose pour un nombre d'individus
          suffisament grand dans chaque groupe (> 30)
        - Normalité vérifiée pour les variables BMI et SleepTime
        - Normalité non vérifiée pour les variables PhysicalHealth et MentalHealth que l'on passe en catégorielles
"""

# Génération des graphiques
fig, axs = plt.subplots(2, 2) # HeartDisease = Yes
axs[0, 0].hist(data[data['HeartDisease'].isin(['Yes'])]['BMI'], edgecolor = 'black', bins = 50) ; axs[0, 0].set_title('BMI')
axs[0, 1].hist(data[data['HeartDisease'].isin(['Yes'])]['PhysicalHealth'], edgecolor = 'black', bins = 50) ; axs[0, 1].set_title('PhysicalHealth')
axs[1, 0].hist(data[data['HeartDisease'].isin(['Yes'])]['MentalHealth'], edgecolor = 'black', bins = 50) ; axs[1, 0].set_title('MentalHealth')
axs[1, 1].hist(data[data['HeartDisease'].isin(['Yes'])]['SleepTime'], edgecolor = 'black', bins = 50) ; axs[1, 1].set_title('SleepTime')
plt.show()

fig, axs = plt.subplots(2, 2) # HeartDisease = No
axs[0, 0].hist(data[data['HeartDisease'].isin(['No'])]['BMI'], edgecolor = 'black', bins = 50) ; axs[0, 0].set_title('BMI')
axs[0, 1].hist(data[data['HeartDisease'].isin(['No'])]['PhysicalHealth'], edgecolor = 'black', bins = 50) ; axs[0, 1].set_title('PhysicalHealth')
axs[1, 0].hist(data[data['HeartDisease'].isin(['No'])]['MentalHealth'], edgecolor = 'black', bins = 50) ; axs[1, 0].set_title('MentalHealth')
axs[1, 1].hist(data[data['HeartDisease'].isin(['No'])]['SleepTime'], edgecolor = 'black', bins = 50) ; axs[1, 1].set_title('SleepTime')
plt.show()

# """ Ajustement des variables PhysicalHealth et MentalHealth """
# data['PhysicalHealth_0'] = [1 if x == 0 else 0 for x in data['PhysicalHealth'].tolist()]
# data['PhysicalHealth_1_29'] = [1 if x > 0 and x < 30 else 0 for x in data['PhysicalHealth'].tolist()]
# data['PhysicalHealth_30'] = [1 if x == 30 else 0 for x in data['PhysicalHealth'].tolist()]
#
# data['MentalHealth_0'] = [1 if x == 0 else 0 for x in data['MentalHealth'].tolist()]
# data['MentalHealth_1_29'] = [1 if x > 0 and x < 30 else 0 for x in data['MentalHealth'].tolist()]
# data['MentalHealth_30'] = [1 if x == 30 else 0 for x in data['MentalHealth'].tolist()]
#
# data = data.drop(columns = ["PhysicalHealth", "MentalHealth"])

"""
    Homoscédasticité :
        - Egalité des variances dans les deux groupes
        - Non vérifiée mais on s'en affranchi du fait que les échantillons n'ont pas été
          créé de manière aléatoire mais sur la base d'une variable.
"""
# Test de Bartlett
bartlett(data[data['HeartDisease'].isin(['Yes'])]["BMI"], data[data['HeartDisease'].isin(['No'])]["BMI"])
# Différence significative des variances entre les deux groupes
bartlett(data[data['HeartDisease'].isin(['Yes'])]["SleepTime"], data[data['HeartDisease'].isin(['No'])]["SleepTime"])
# Différence significative des variances entre les deux groupes


