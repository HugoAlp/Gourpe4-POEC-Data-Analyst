# **Projet Big Data - Groupe 4**
Morgane Geoffroy - Hugo Alpiste - Yen Phi DO - Sébastien MARTEL

## **Features**

- Runs on Windows
- The application deploys 3 Docker containers with Hadoop preconfigured (1 Namenode + 2 slaves).
- It aims at processing datasets provided by our trainer Christophe Germain, in order to produce visualisations bringing valuable medical insights.
- Due to configuration issues and lack of time, we could not link our Hadoop database to any ELK solution, so got the data out manually (see "data_powerbi.csv") and went through the visualisations using Power BI.

---

## **Configuration**

**Requirements:**

- An installation of **Docker desktop** is required to use _Projet Big Data_. The **Docker desktop** installation process can be checked on https://docs.docker.com/desktop/install/windows-install/
- **python** **(version 3.9 or above)** is also required to access _Projet Big Data_. If your system does not have a **python** distribution, it can be downloaded from https://www.python.org/downloads/.
- **pip** is required for installing the dependencies.
- **Power BI Desktop** is necessary to display the data visualisations.

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
git clone https://github.com/mgeoff93/Diginamic---Projet-Hadoop.git
```

- Install the dependencies listed in requirements.in:

```sh
pip install -r requirements.in
```

- Launch Docker desktop
  
- Run the setup.ps1

**This will setup the application and preprocess the data.**

- Then connect to the hadoop-master container and locally launch the mapper and reducer to send the data in hbase:
```sh
docker exec -it hadoop-master bash

cat data.csv | python3 mapper.py | python3 reducer.py
```
- (The hadoop-streaming jar breaks down when we include any connexion to hbase.)

**Visualisations**
- The visualisations are setup in the "Dashboard - Projet Big Data.pbix" file (requires Power BI Desktop).
- The Power Query part can be checked using the file assets/data/data_powerbi.csv .

---

## **Dependencies**

For this project, the **requirements.in** file lists the Python dependencies.

- happybase **(version 1.2.0)**

- pandas **(version 2.0.3)**

- hdfs **(version 2.7.0)**

- python-dotenv **(version 1.0.0)**

- xlrd **(version 2.0.1)**

---

## **Data description**

We initially have 5 data files:

- **DATA-SUIVICGE.XLS**
    Basic information about the patient, the initial medical consultation and the resulting prescription.
  - **SUCLE_REF:** SuiviCle is the Primary Key of the suivi table, this column makes the link with the alim_lsuivi.csv table.
  - **SUCOD_REF:** SuiviCode is a complement of the primary key.
  - **PACLE_REF:** Identifies a patient as a key
  - **SVNATURE:** Identifies a predefined type of follow-up
  - **SVTYPE:** Identifies a predefined follow-up type
  - **SVMODE:** Transcribes an emergency scale with a predefined breakpoint
  - **SVDATE:** Follow-up date
  - **SVDUREE:** Duration of follow-up
  - **SVPOIDS:** Weight of monitored patient
  - **SVTAILLE:** Height of monitored patient
  - **AGEENJOUR:** Patient's age in days
  - **GDGROUPE:** Code identifying the patient in one of the predefined groups according to sex, age, etc.
  - **DGCLE_REF:** Key corresponding to the patient's diagnosis
  - **SVPROT_A, SVPROT_V, SVAAM, SVLIP, SVGLU, SVCAL, SVCA, SVP, SVNA, SVK, SVFE, SVMG, :** Amounts of different nutrients: proteins, amino-acids, lipids, carbohydrates...
  - **DGCODE:** Code corresponding to diagnosis

- **DATA-LSUIVICGE.XLS**
    Any SUIVICGE can have 0 to multiple LSUIVICGEs. These ones describe the aliments fed to the patient in accordance with the prescription.
  - **LSCLE_REF:** Primary key of table lsuivi.
  - **SUCLE_REF:** Foreign key to the DATA-SUIVICGE table.
  - **NOMODE:** Nutrition mode
  - **NBREMODE:** Quantity/100
  - **QUANTITE:** Quantity of food given to the patient during follow-up
  - **REPAS:** Code referencing predefined meal times
    
- **DIAG.XLS**
    Description of the diseases as per the digagnosis in the SUIVICGE.
  
- **ALIMENT.XLS**
    Description of the aliments and their characteristics in regard of the different diets.
  - **ALCLE_REF:** Primary key of the food table
  - **TYPE:** Food type code
  - **NOM_ALIM:** Food name
  - **FAMILLE_AL:** Code corresponding to predefined food families
  - **SSFAM_AL:** Code corresponding to predefined food subfamilies
  - **FOURNISSEU :** Numeric code corresponding to predefined suppliers
  - **ORIGINE :** Defined by a code indicating the origin of a food item
  - **DATE_AL:** Food registration date
  - **QUANTITE_A :** Quantity of a standard portion of the aliment
  - **NOMODE:** Code corresponding to the method of feeding
  - **POIDS_AL:** Reference weight of food for calculation purposes
  - **HYPERCAL, HYPERPROT, HYPOCAL, HYPOLIP, HYPOPROT, SANSGLUTEN, SANSSEL, SANSSUCRE:** Booleans specifying whether the product is adequate for each diet (regarding respectively calories, proteins, lipids, gluten, salt and sugar).

- **VOLCODE.XLS**
    A contingency table providing codes to labels conversions and information on the relational junctions between the other tables.
    - **VCCODE:** Alphanumeric code corresponding to VCTYPEs and VCLIBELLEs
    - **VCLIBELLE, VCTYPE:** Supplier, food, alimentation mode and products packaging labels
