""" Importation des librairies """
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
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
from sklearn.pipeline import Pipeline

logReg = LogisticRegression(max_iter = 10000)
pipe = Pipeline(steps=[('logistic_Reg', logReg)])
C = np.logspace(0, 2, 50)
penalty = ['l1', 'l2', None]
parameters = dict(logistic_Reg__C = C,
                  logistic_Reg__penalty = penalty)
logReg_gscv = GridSearchCV(pipe, parameters).fit(X, y)
logReg_opti = logReg_gscv.best_estimator_
logReg_gscv.best_score_ # 0.9159492800075049

""" Prédictions """
y_pred = logReg_opti.predict(X_test)

""" Accuracy """
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, y_pred) # 0.9163716869504309

""" Sauvegarde du modèle """
from joblib import dump
dump(logReg_opti, "scripts/machineLearning/logReg_opti.joblib")

""" Bon modèle qui n'underfit ou n'overfit pas """
