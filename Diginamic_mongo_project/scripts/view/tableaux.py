import os
tmp_path = os.getcwd().split("Diginamic_mongo_project")[0]
target_path = os.path.join(tmp_path, 'Diginamic_mongo_project')
import sys
sys.path[:0] = [target_path]
from tkinter import *
from tkinter import ttk
import pandas as pd
from scripts.utils import *


def export_excel(tableau: ttk.Treeview, colonnes: list):
        data_list = []
        for child in tableau.get_children():
                data_list.append(dict(zip(colonnes, tableau.item(child)["values"])))

        data_df = pd.DataFrame.from_dict(data_list)
        data_df.to_excel(os.path.join(ASSETS_PATH, "export.xlsx"), index=False)

def export_csv(tableau: ttk.Treeview, colonnes: list):
        data_list = []
        for child in tableau.get_children():
                data_list.append(dict(zip(colonnes, tableau.item(child)["values"])))

        data_df = pd.DataFrame.from_dict(data_list)
        data_df.to_csv(os.path.join(ASSETS_PATH, "export.csv"), index=False)

def generate_buttons(onglet: ttk.Frame, tableau: ttk.Treeview, colonnes: list):
        """
        Génère les boutons d'export sur l'onglet data
        """
        bt_excel =Button (onglet,text= "Exporter: xlsx" ,command=lambda : export_excel(tableau, colonnes) ,activebackground='green', height=2 , width=20)
        bt_excel.grid(column=1100, row=550)

        bt_csv =Button (onglet,text= "Exporter: csv" ,command=lambda : export_csv(tableau, colonnes) ,activebackground='green', height=2 , width=20)
        bt_csv.grid(column=1400, row=550, pady=540)

def create_tableau(onglet: ttk.Frame, patients_data: list, valeurs_combo: dict):
        """
        Génère le contenu de l'onglet data
        """
        texte_vide = (' '*150+"\n")*4
        ttk.Label(onglet, text =texte_vide).grid(
                column = 0,  row = 0, padx = 30, pady = 30) 
        nb_patients = len(patients_data)
        phrase_criteres = "Filtres actifs :\n" + str(valeurs_combo).strip("{}").replace("'", '') + "\nRésultats: " + str(nb_patients)
        ttk.Label(onglet, text=phrase_criteres).grid(
                column = 0,  row = 0, padx = 30, pady = 30)
        
        # Ss'il y a des patients correspondant au filtre, on génère le tableau
        if nb_patients:

                # Création du tableau
                print("Tableau: génération")
                tableau = ttk.Treeview(onglet)
                colonnes = tuple(patients_data[0].keys())
                tableau['columns'] = colonnes
                tableau['show'] = "headings"

                ancre = "center"
                for titre in colonnes:
                        tableau.column(titre, anchor=ancre, width=80)
                        tableau.heading(titre, text=titre, anchor=ancre)

                # Remplissage avec les données. Compteur pour afficher la progression
                print("Tableau: remplissage...")
                cpt = 0
                for patient in patients_data:
                        cpt += 1
                        if not cpt %20000:
                                print(cpt)
                        tableau.insert(parent='', index='end', text="", values=([patient[clef] for clef in colonnes]))

                print("Tableau: fin de remplissage.")

                # Positionnement et génération des boutons
                tableau.place(relx=0.01, rely=0.1, width=1460, height=500)
                generate_buttons(onglet, tableau, colonnes)


