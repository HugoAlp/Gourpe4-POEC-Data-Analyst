import sys
import happybase

# line = "1,NECKER001,1225,2,3,1,2002-05-02 00:00:00,0,8.28,69.0,265,1BE,7,4.8,0.0,0.0,29.85,59.4,525.0,560.0,356.5,8.9,15.4,7.85,61.5,AIV,ACIDEMIE ISOVALERIQUE,3.0,ENFANT 6 MOIS A 1 AN,6M-1A,152.0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"

for line in sys.stdin:

    # List of fields
    fields = ["SUCLE_REF","SUCOD_REF","PACLE_REF","SVNATURE","SVTYPE","SVMODE","SVDATE","SVDUREE","SVPOIDS","SVTAILLE","AGEENJOUR","GDGROUPE",
              "DGCLE_REF","SVPROT_A","SVPROT_V","SVAAM","SVLIP","SVGLU","SVCAL","SVCA","SVP","SVNA","SVK","SVFE","SVMG","DGCODE","DGLIBELLE","DGTYPE",
              "VCLIBELLE_G","VCABREGE_G","VCNUMERO_G","ALCLE_REF","LSCLE_REF","NOMODE_LSUIVI","NBREMODE","QUANTITE","REPAS","TYPE","NOM_ALIM",
              "FAMILLE_AL","SSFAM_AL","FOURNISSEU","ORIGINE","DATE_AL","QUANTITE_A","NOMODE_ALIM","POIDS_AL","HYPERCAL","HYPERPROT","HYPOCAL",
              "HYPOLIP","HYPOPROT","SANSGLUTEN","SANSSEL","SANSSUCRE","VCCODE_F","VCLIBELLE_F","VCTYPE_M","VCCODE_M","VCLIBELLE_M","VCABREGE_M"]

    # Split the line into fields and remove leading and trailing whitespaces
    incoming_fields = [field.strip() for field in line.split(",")]

    # List creation
    liste = list()
    for column in ["QUANTITE", "SVPOIDS", "SVTAILLE", "AGEENJOUR", "SUCOD_REF"] :
        if column == "SVPOIDS" :
            if len(incoming_fields[fields.index(column)]) > 0 and float(incoming_fields[fields.index(column)]) > 0 : liste.append(True)
            else : liste.append(False)
        elif column == "QUANTITE" :
            if len(incoming_fields[fields.index(column)]) == 0 or float(incoming_fields[fields.index(column)]) > 0 : liste.append(True)
            else : liste.append(False)
        elif column in ["SVTAILLE", "AGEENJOUR"]:
            if len(incoming_fields[fields.index(column)]) == 0 or float(incoming_fields[fields.index(column)]) >= 0 : liste.append(True)
            else : liste.append(False)
        else :
            if incoming_fields[fields.index("SUCOD_REF")] == "NECKER001" : liste.append(True)
            else : liste.append(False)
    
    # Line display
    if all(liste) :
        del incoming_fields[fields.index("SUCOD_REF")]
        print(",".join(incoming_fields))