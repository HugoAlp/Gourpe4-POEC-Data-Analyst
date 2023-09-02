# **MedicalAssistant_V2**
Nouvelle version du projet Diginamic MedicalAssistant: https://github.com/HugoAlp/Diginamic_mongo_project.git

Cette fois-ci, exploration et Machine Learning sur ce jeu de données médicales obtenu sur Kaggle:
https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease

Le but sera de prédire, sur la saisie d'une liste de critères médicaux, si le patient est prédisposé à être touché d'une maladie cardiaque ou non.

## **Authors**

Geoffroy Morgane
Do Yen Phi
Martel Sebastien
Alpiste Hugo

## **Configuration**

**Requirements:**

- The application runs on Windows 10+

- An installation of **MongoDB** **(version 3.4.0 or above)** is required to use _MedicalAssistant_. The **MongoDB** installation can be downloaded from https://www.mongodb.com/docs/manual/installation/
- **python** **(version 3.6 or above)** is also required to access _MedicalAssistant_. If your system does not have a **python** distribution, it can be downloaded from https://www.python.org/downloads/.
- **pip** is required for installing the dependencies.

**Installation:**

- Create a virtual environment:

```sh
python -m venv venv
```

```sh
venv\Scripts\activate
```

- Open a shell in the folder that hosts the newly created virtual environment and download the project:

```sh
git clone https://github.com/HugoAlp/MedicalAssistant_V2.git
```

- Create your .env file based on .env-template
- Install the dependencies listed in requirements.in:

```sh
pip install -r requirements.in
```

- Run the setup:
```sh
python -m setup.py
```
This deploys the data in the MongoDB base.
- Launch the application:
```sh
python -m streamlit run MEDICAL_ASSISTANT.py
```
![Alt text](a481c866-c98d-408b-b2c1-de7efcbea95e.jpg)

press enter to skip this step

**The application will launch and you can now use it.**
Fill up the patient's data, submit and get the prediction.

---

## **Dependencies**

For this project, the **requirements.in** file lists the Python dependencies.

- matplotlib **(version 3.7.1)**

- pandas **(version 2.0.2)**

- pymongo **(version 4.3.3)**

- python-dotenv **(version 1.0.0)**

- seaborn **(version 0.12.2)**

- tqdm **(version 4.65.0)**

---

## **Data description**

The project utilizes the following data attributes:

- **Heart disease:** Indicates whether respondents have ever reported having coronary heart disease (CHD) or myocardial infarction (MI)

- **BMI:** Body Mass Index (BMI)

- **Smoking:** Determines if respondents have smoked at least 100 cigarettes in their lifetime. (Note: 5 packs = 100 cigarettes)

- **Alcohol drinking:** Indicates whether respondents are considered heavy drinkers. (Note: For adult men, heavy drinking refers to consuming more than 14 drinks per week, while for adult women, it means consuming more than 7 drinks per week)

- **Stroke:** Indicates whether respondents have ever suffered a stroke

- **Physical health:** Reflects the number of days during the past 30 days when respondents experienced poor physical health, including illness and injury

- **Mental health:** Indicates the number of days during the past 30 days when respondents experienced poor mental health

- **Walking difficulty:** Determines if respondents have serious difficulty walking or climbing stairs

- **Sex:** Identifies respondents' gender as male or female

- **Age category:** Represents respondents' age categorized into fourteen levels

- **Ethnicity:** Indicates the imputed race/ethnicity value

- **Diabetes:** Determines if respondents have ever had diabetes

- **Physical activity:** Indicates whether respondents have engaged in physical activity or exercise during the past 30 days, excluding regular job-related activities

- **General health:** Reflects respondents' perception of their overall general health

- **Sleep time:** Represents the average number of hours of sleep obtained within a 24-hour period

- **Asthma:** Determines if respondents have ever been told they had asthma.

- **Kidney disease:** Indicates if respondents have ever been diagnosed with kidney disease, excluding kidney stones, bladder infections, or incontinence

- **Skin cancer:** Determines if respondents have ever been told they had skin cancer
---
## **Project structure**



- MEDICAL_ASSISTANT.py **(Source code of web app)**

- requirements.in **(Listing all Python dependencies for this project)**

- setup.py **(build mongo database and )**

- assets **(Contain data's csv )**

- scripts **(contain project's scripts)**
  - explore **(exploratory analysis )**
    - img **(Gaphs generated in png)**
    - dataPreprocessing.py
    - devScript.py
    - exploration_graphs.py
  - machineLearning **(contain machine learnig's scripts)**
    - knn.py
    - logReg.py
    - randomForest.py
  - models **(Database connexion)**
  - utils.py **(recurent functions and variable needed on project)**