import sys
import happybase

# line = "1,1225,2,3,1,2002-05-02 00:00:00,0,8.28,69.0,265,1BE,7,4.8,0.0,0.0,29.85,59.4,525.0,560.0,356.5,8.9,15.4,7.85,61.5,AIV,ACIDEMIE ISOVALERIQUE,3.0,ENFANT 6 MOIS A 1 AN,6M-1A,152.0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"

# Champs
fields = ["SUCLE_REF","PACLE_REF","SVNATURE","SVTYPE","SVMODE","SVDATE","SVDUREE","SVPOIDS","SVTAILLE","AGEENJOUR","GDGROUPE",
          "DGCLE_REF","SVPROT_A","SVPROT_V","SVAAM","SVLIP","SVGLU","SVCAL","SVCA","SVP","SVNA","SVK","SVFE","SVMG","DGCODE","DGLIBELLE","DGTYPE",
          "VCLIBELLE_G","VCABREGE_G","VCNUMERO_G","ALCLE_REF","LSCLE_REF","NOMODE_LSUIVI","NBREMODE","QUANTITE","REPAS","TYPE","NOM_ALIM",
          "FAMILLE_AL","SSFAM_AL","FOURNISSEU","ORIGINE","DATE_AL","QUANTITE_A","NOMODE_ALIM","POIDS_AL","HYPERCAL","HYPERPROT","HYPOCAL",
          "HYPOLIP","HYPOPROT","SANSGLUTEN","SANSSEL","SANSSUCRE","VCCODE_F","VCLIBELLE_F","VCTYPE_M","VCCODE_M","VCLIBELLE_M","VCABREGE_M"]

# Connexion à la base
connection = happybase.Connection('127.0.0.1', port = 9090)

# Création de la table si elle n'existe pas
if bytes('{}'.format("supertable"), 'utf-8') not in connection.tables() : connection.create_table(name = 'supertable', families = dict(zip(['SUIVI', 'LSUIVI'], [dict()]*2)))

# Connexion à la table
# table = connection.table('supertable')

for line in sys.stdin :
    
    line = line.rstrip("\n").split(",")
    
    rowkey = bytes('{}'.format(line[0]) + "-" + '{}'.format(line[31]), 'utf-8')

    connection = happybase.Connection('127.0.0.1', port = 9090)
    table = connection.table('supertable')
    if len(table.row(rowkey)) != 0 : 
        continue ############################################ Break ou continue ?
    else :
        keys = [bytes('SUIVI:{}'.format(fields[i]), 'utf-8') for i in range(0, 30)] + [bytes('LSUIVI:{}'.format(fields[i]), 'utf-8') for i in range(31, len(fields))]
        try :
            values = [bytes('{}'.format(line[i]), 'utf-8') for i in range(0, 30)] + [bytes('LSUIVI:{}'.format(line[i]), 'utf-8') for i in range(31, len(fields))]
        except UnicodeEncodeError as err :
            if '/udcc3' in str(err) : continue
        params = dict(zip(keys, values))
        
        connection = happybase.Connection('127.0.0.1', port = 9090)
        table = connection.table('supertable')
        table.put(row = rowkey, data = params)
        print("RowKey: {}, statut: OK".format(line[0] + "-" + line[31]))