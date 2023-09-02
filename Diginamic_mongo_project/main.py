from scripts.view.heart import *
    
# Caractéristiques de notre fenètre 
fen  = Tk()
fen.title('Medical assistant - Databradors')
fen.geometry('1500x800')
fen.resizable(width=True,height=True)
style = ttk.Style()
style.theme_use('alt') # clam, step, alt, classic
style.configure("Treeview.Heading", background="DarkSlateGray1")


#on définit les onglet 
ong_control=ttk.Notebook(fen)
request = ttk.Frame(ong_control)
data = ttk.Frame(ong_control)


ong_control.add(request, text='Request',)
ong_control.add(data, text='Data')


ong_control.pack(expand=1,fill="both")

#on dispose un label dans chaque onglet
ttk.Label(request, 
        text ="Bienvenue dans l'onglet request").grid(column = 0, 
                            row = 0,
                            padx = 30,
                            pady = 30)  

lab_titre=Label(fen,
                text= "L'assistant médical qui se base sur la Data !",
                height=1,
                relief=SUNKEN,
                fg='white',
                font= ("Calibri",18),
                bg="green"
                )
lab_titre.pack()
# frame 1
IRequests = Frame(request, borderwidth=2, relief=GROOVE )
IRequests.grid(column=2)

#a refaire avec un jolie boucle si on a le temps 
dict_combo= {}
id_fin=1
for index, column in enumerate(ALL_COLL):
    Label(IRequests, text=COLNAMES_DICT[column]+" :",font='Calibri', padx=50,justify='left').grid(row= index ,column=0)
    combo_label= column+"_combolabel"
    combobox = ttk.Combobox(IRequests, textvariable=combo_label)
    match column:
        case 'Sex':
            combobox['values'] = ["Male","Female"]
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
        case 'AgeCategory':
            combobox['values'] = ['18-24','25-29', '30-34','35-39','40-44', '45-49', '50-54','55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
        case 'Race':
            combobox['values'] = ['White', 'Black', 'Asian', 'American Indian/Alaskan Native', 'Other', 'Hispanic']
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
        case 'Diabetic':
            combobox['values'] = ['Yes', 'No', 'No, borderline diabetes', 'Yes (during pregnancy)']
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
        case 'GenHealth':
            combobox['values'] = ['Very good', 'Fair', 'Good', 'Poor', 'Excellent']
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
        case 'PhysicalHealth'|'MentalHealth':
            combobox['values'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
        case 'SleepTime':
            combobox['values'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
        case 'BMI':
            
            combobox['values'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
                                21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
                                41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,
                                61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,
                                81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
        case _:
            combobox['values'] = ["No","Yes"]
            combobox['state'] = 'readonly'
            combobox['width']= 30
            dict_combo[combo_label] = combobox
            combobox.grid(row= index ,column=1)
    id_fin+=1
    
bt_valid =Button (request,text= "Find" ,command=lambda :click(db_heart,img_path,dict_combo, data, request) ,activebackground='green', height=2 , width=20)
bt_valid.grid(column=3)

bt_clear =Button (request,text= "Clear" ,command=lambda :click_clear(dict_combo, request) ,activebackground='green', height=2 , width=20)
bt_clear.grid(column=3)

fen.mainloop()
