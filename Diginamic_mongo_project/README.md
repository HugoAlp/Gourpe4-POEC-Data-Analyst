# **MedicalAssistant (MA)**

## **Authors**

Geoffroy Morgane
Do Yen Phi
Martel Sebastien 
Alpiste Hugo

## **Features**

- Runs on Windows

---

## **Configuration**

**Requirements:**

- An installation of **MongoDB** **(version 3.4.0 or above)** is required to use _MedicalAssistant_. The **MongoDB** installation can be downloaded from https://www.mongodb.com/docs/manual/installation/
- **python** **(version 3.6 or above)** is also required to access _MedicalAssistant_. If your system does not have a **python** distribution, it can be downloaded from https://www.python.org/downloads/.
- **pip** is required for installing the dependencies.

**Installation:**

- Create a virtual environment:

```sh
python -m venv localEnv
```

```sh
localEnv\Scripts\activate
```

- Open a shell in the folder that hosts the newly created virtual environment and download the project:

```sh
git clone https://github.com/HugoAlp/Diginamic_mongo_project.git
```

- Create your .env file based on .env-template
- Install the dependencies listed in requirements.in:

```sh
pip install -r requirements.in
```

- Run the setup.py
- Run the main.py

**The application will launch and you can now use it.**

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
