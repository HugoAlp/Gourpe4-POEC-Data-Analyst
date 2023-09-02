""" Importation des librairies """
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from scripts.explore.dataPreprocessing import dataPreprocessing
import time

""" Importation des données """
data = dataPreprocessing()

""" Définition des features et de la target """
X = data.drop(columns = ['HeartDisease'], axis = 1)
y = data['HeartDisease'].values

""" Split """
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 1, stratify = y)

""" Optimisation des paramètres """
from sklearn.model_selection import GridSearchCV

knn = KNeighborsClassifier()
param_grid = {'n_neighbors': np.arange(1, 50)}
knn_gscv = GridSearchCV(knn, param_grid, cv = 4).fit(X_train, y_train)
knn_opti = knn_gscv.best_estimator_
knn_gscv.best_score_ # 0.915153891867322

""" Prédictions """
y_pred = knn_opti.predict(X_test)

""" Accuracy """
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, y_pred) # 0.9156337164942651

""" Sauvegarde du modèle """
from joblib import dump
dump(knn_opti, "scripts/machineLearning/knn_opti.joblib")

""" Bon modèle qui n'underfit ou n'overfit pas """