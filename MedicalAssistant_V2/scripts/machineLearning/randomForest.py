from joblib import dump
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
import sys
tmp_path = os.getcwd().split("MedicalAssistant_V2")[0]
target_path = os.path.join(tmp_path, 'MedicalAssistant_V2')
sys.path[:0] = [target_path]
from scripts.explore.dataPreprocessing import dataPreprocessing

df = dataPreprocessing()

X = df.drop(columns=["HeartDisease"])
y = df["HeartDisease"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

model = RandomForestClassifier()
# Les hyperparamètres testés ci-dessous ont été obtenus après plusieurs passes
hyperparams = {'n_estimators': [600, 730, 800], 'max_features': list(range(1, 3))}
best_model = GridSearchCV(model, hyperparams, cv = 5, n_jobs=-1).fit(X_train, y_train)

dump(best_model, 'randomForest_opti.joblib')

print('Score du GridSearch:', best_model.best_score_, 'params:', best_model.best_params_, 'estim:', best_model.best_estimator_) 

""" Prédictions """
y_pred = best_model.predict(X_test)

""" Accuracy """
acc = accuracy_score(y_test, y_pred)
print("Accuracy testée: ", acc)

# Les résultats obtenus en GridSearch et en prédiction étant similaires, ce modèle ne semble ni overfitter, ni underfitter.
# Toutefois, en raison de meilleurs résultats obtenus avec les autres modèles testés, le RandomForest n'a au final pas été retenu.





