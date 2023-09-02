import os
import pandas as pd

# functions ---|
def clean_espaces(df):
    df_obj_cols = list(df.select_dtypes(include='object'))
    df_str_cols = [col for col in df_obj_cols if "date" not in col.lower()]
    df[df_str_cols] = df[df_str_cols].apply(lambda x: x.str.strip())

def del_dupli_pk(df, pk_col):
    df.drop_duplicates(subset=pk_col, inplace=True, ignore_index=False)

def filtre_cols(df, filtre):
    for column, filter in filtre.items():
        if filter[0]:
            df = df[df[column] == filter[1]]
        else:
            df = df[df[column] != filter[1]]
    return df

def manage_columns(df, colonnes, remove=True):
    if remove:
        df = df.drop(columns=colonnes, inplace=True)
    else:
        df = df[colonnes]
    return df

def compar_uniqs(cola, colb):
    valsa = set(cola)
    valsb = set(colb)
    diff = valsa-valsb
    print(diff)
    print(len(diff))

# Data import ---|
print("Collecte des fichiers...")

data_folder = os.path.join("assets","data")
data_suivi_path = os.path.join(data_folder, "DATA-SUIVICGE.XLS")
data_lsuivi_path = os.path.join(data_folder, "DATA-LSUIVICGE.XLS")
data_diag_path = os.path.join(data_folder, "DIAG.XLS")
data_alim_path = os.path.join(data_folder, "ALIMENT.XLS")
volcode_path = os.path.join(data_folder, "VOLCODE.XLS")

suivi_df = pd.read_excel(data_suivi_path)
lsuivi_df = pd.read_excel(data_lsuivi_path)
diag_df = pd.read_excel(data_diag_path)
alim_df = pd.read_excel(data_alim_path)
volcode_df = pd.read_excel(volcode_path)

# Vérification de l'unicité des clés primaires
del_dupli_pk(suivi_df, "SUCLE_REF")
del_dupli_pk(lsuivi_df, "LSCLE_REF")
del_dupli_pk(diag_df, "DGCLE_REF")
del_dupli_pk(alim_df, "ALCLE_REF")

clean_espaces(suivi_df)
clean_espaces(lsuivi_df)
clean_espaces(diag_df)
clean_espaces(alim_df)
clean_espaces(volcode_df)

# Suppression initiale de colonnes
keep_cols_diag = ["DGCLE_REF", "DGCODE","DGLIBELLE", "DGTYPE"]
diag_df = manage_columns(diag_df, keep_cols_diag, remove=False)

# Keep columns aliment
keep_cols_alims = [
    "ALCLE_REF","TYPE","NOM_ALIM","FAMILLE_AL","SSFAM_AL","FOURNISSEU","ORIGINE","DATE_AL",
    "QUANTITE_A","NOMODE","POIDS_AL","HYPERCAL","HYPERPROT","HYPOCAL","HYPOLIP",
    "HYPOPROT","SANSGLUTEN","SANSSEL","SANSSUCRE",
]
alim_df = manage_columns(alim_df, keep_cols_alims, remove=False)

# Keep columns volcode
keep_cols_volcode = [
    "VCTYPE","VCCODE","VCLIBELLE","VCABREGE","VCNUMERO"
]
volcode_df = manage_columns(volcode_df, keep_cols_volcode, remove=False)

# Keep columns suivi
keep_cols_suivi = ["SUCLE_REF","SUCOD_REF","PACLE_REF","SVNATURE","SVTYPE","SVMODE","SVDATE",
                   "SVDUREE","SVPOIDS","SVTAILLE","AGEENJOUR","GDGROUPE","DGCLE_REF",
                   "SVPROT_A","SVPROT_V","SVAAM","SVLIP","SVGLU","SVCAL","SVCA","SVP","SVNA","SVK",
                   "SVFE","SVMG"
]

suivi_df = manage_columns(suivi_df, keep_cols_suivi, remove=False)

# Keep columns lsuivi

keep_cols_lsuivi = [
    "ALCLE_REF", "SUCLE_REF", "LSCLE_REF", "NOMODE","NBREMODE","QUANTITE","REPAS"
]
lsuivi_df = manage_columns(lsuivi_df, keep_cols_lsuivi, remove=False)

# Jointures
print("Réalisation des jointures...")

# alim-> lsuivi: alcle_ref
alim_lsuivi_df = lsuivi_df.merge(alim_df, on="ALCLE_REF", how="left")

# diag "DGCLE_REF" -> suivi[dgcle_ref]
diag_suivi_df = suivi_df.merge(diag_df, on="DGCLE_REF", how="left")

# Rename columns alim_lsuivi_df
alim_lsuivi_df.rename(columns={"NOMODE_x": "NOMODE_LSUIVI", "NOMODE_y": "NOMODE_ALIM"}, inplace = True)

# Conversion des types de colonnes
integers = ["SVNATURE", "SVTYPE", "SVMODE"]
for i in integers : diag_suivi_df[i] = pd.Series(diag_suivi_df[i], dtype=pd.Int64Dtype())

integers = ["LSCLE_REF", "REPAS", "TYPE", "FAMILLE_AL", "SSFAM_AL", "FOURNISSEU", "QUANTITE_A", "NOMODE_ALIM"] # Ajouter LSCLEREF ?
booleans = ["HYPERCAL", "HYPERPROT", "HYPOCAL", "HYPOLIP", "HYPOPROT", "SANSGLUTEN", "SANSSEL", "SANSSUCRE"]
for i in integers : alim_lsuivi_df[i] = pd.Series(alim_lsuivi_df[i], dtype=pd.Int64Dtype())
for i in booleans : alim_lsuivi_df[i] = pd.Series(alim_lsuivi_df[i], dtype=pd.BooleanDtype())

# Fichiers intermédiaires
als = alim_lsuivi_df
ds = diag_suivi_df
vc = volcode_df

# Merge als
inter = vc.iloc[[x for x in range(0, len(vc["VCTYPE"])) if vc["VCTYPE"][x] == "F"]]
als = als.merge(inter, left_on = "FOURNISSEU", right_on = "VCNUMERO", how = "left")

inter = vc.iloc[[x for x in range(0, len(vc["VCTYPE"])) if vc["VCTYPE"][x] == "M"]]
als = als.merge(inter, left_on = "NOMODE_LSUIVI", right_on = "VCNUMERO", how = "left")

# Merge ds
inter = vc.iloc[[x for x in range(0, len(vc["VCTYPE"])) if vc["VCTYPE"][x] == "G1"]]
ds = ds.merge(inter, left_on = "GDGROUPE", right_on = "VCCODE", how = "left")

inter = vc.iloc[[x for x in range(0, len(vc["VCTYPE"])) if vc["VCTYPE"][x] == "G2"]]
ds = ds.merge(inter, left_on = "GDGROUPE", right_on = "VCCODE", how = "left")

inter = vc.iloc[[x for x in range(0, len(vc["VCTYPE"])) if vc["VCTYPE"][x] == "G3"]]
ds = ds.merge(inter, left_on = "GDGROUPE", right_on = "VCCODE", how = "left")

# Fusion columns ds
cols_fusion = ["VCCODE", "VCLIBELLE", 'VCABREGE', 'VCNUMERO']
for colonne in cols_fusion:
    ds[f"{colonne}_G"] = ds.apply(lambda row: row[f"{colonne}_x"] if pd.notna(row[f"{colonne}_x"]) else row[f"{colonne}_y"] if pd.notna(row[f"{colonne}_y"]) else row[colonne], axis = 1)

# Drop columns ds
dropped_col_ds = ['VCTYPE_x', 'VCCODE_x', 'VCLIBELLE_x', 'VCABREGE_x',
                  'VCNUMERO_x', 'VCTYPE_y', 'VCCODE_y', 'VCLIBELLE_y',
                  'VCABREGE_y', 'VCNUMERO_y', 'VCTYPE', 'VCCODE', 'VCLIBELLE',
                  'VCABREGE', 'VCNUMERO', 'VCCODE_G']

ds = ds.drop(dropped_col_ds, axis = 1)

# Rename columns als
rename_col_als = {'VCTYPE_x' : 'VCTYPE_F', 'VCCODE_x' : 'VCCODE_F', 'VCLIBELLE_x' : 'VCLIBELLE_F', 'VCABREGE_x' : 'VCABREGE_F',
                  'VCNUMERO_x' : 'VCNUMERO_F', 'VCTYPE_y' : 'VCTYPE_M', 'VCCODE_y' : 'VCCODE_M', 'VCLIBELLE_y' : 'VCLIBELLE_M',
                  'VCABREGE_y' : 'VCABREGE_M', 'VCNUMERO_y' : 'VCNUMERO_M'}

als = als.rename(columns = rename_col_als)

# Drop columns als
dropped_col_als = ['VCTYPE_F', 'VCABREGE_F', 'VCNUMERO_F', 'VCNUMERO_M']
als = als.drop(dropped_col_als, axis = 1)

# Merge ds avec als
final = ds.merge(als, left_on = "SUCLE_REF", right_on = "SUCLE_REF", how = "left")

# Insert column
# final.insert(0, "ROWKEY", [for x in ], True)

# Exports csv
print("Ecriture des fichiers csv:")
print("Fichier data")
final.to_csv("send_namenode/data.csv", index = False, encoding = "utf-8", header = False)
# print("diag_suivi")
# ds.to_csv("send_namenode/diag_suivi.csv", index = False, encoding = "utf-8")
# print("alim_lsuivi")
# als.to_csv("send_namenode/alim_lsuivi.csv", index = False, encoding = "utf-8")