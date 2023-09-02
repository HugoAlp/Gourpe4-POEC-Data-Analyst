class Patient:

    # instance attributes
    def __init__(self, data):
        """
        Constructeur de la classe Patient
        Initialise les informations du patient
        Args :
            data (dict): Les informations du patient
        """
        self.info=data
        # convertit les attributs BMI, PhysicalHealth, MentalHealth et SleepTime en valeurs flottantes
        for nom_col in ('BMI','PhysicalHealth','MentalHealth','SleepTime'):
            if self.info.get(nom_col):
                self.info[nom_col] = float(self.info[nom_col]) 
        
    def add_patient(self,collection,patient):
        """
        Ajoute le patient à la collection.
        Args :
            collection: La collection dans laquelle ajouter le patient.
            patient: Le patient à ajouter.
        """
        try :
            collection.insert_one(self.info)
            print('patient est ajouté ')
        # si une erreur se produit, affiche un message d'erreur
        except ValueError as e:
            print(str(e))
            print("le patient n'a pas pu etre ajouté ")
            