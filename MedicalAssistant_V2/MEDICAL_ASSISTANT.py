import os
tmp_path = os.getcwd().split("MEDICALASSISTANT_V2")[0]
target_path = os.path.join(tmp_path, 'MEDICALASSISTANT_V2')
import sys
sys.path[:0] = [target_path]
from joblib import load
import streamlit as st
import pandas as pd
import numpy as np
from scripts.utils import *
import time
from scripts.explore.dataPreprocessing import dataPreprocessing

def runStat():
    result = {'Smoking':  st.session_state.R_smoking[0],
            'AlcoholDrinking': st.session_state.R_AlcoholDrinking[0],
            'Stroke': st.session_state.R_Stroke[0],
            'DiffWalking': st.session_state.R_DiffWalking[0],
            'Sex': st.session_state.R_Sex[0],
            'AgeCategory': st.session_state.SB_AgeCategory[0],
            'Race': st.session_state.SB_Race[0],
            'Diabetic':  st.session_state.SB_Diabetic[0],
            'PhysicalActivity': st.session_state.R_PhysicalActivity[0],
            'GenHealth': st.session_state.SB_GenHealth[0],
            'Asthma': st.session_state.R_Asthma[0],
            'KidneyDisease': st.session_state.R_KidneyDisease[0],
            'SkinCancer': st.session_state.R_SkinCancer[0],
            'BMI':st.session_state.S_BMI[0],
            'PhysicalHealth':st.session_state.S_PhysicalHealth[0],
            'MentalHealth':st.session_state.S_MentalHealth[0],
            'SleepTime':st.session_state.S_Sleep[0]}
    df_dataprocess = dataPreprocessing(result)
    model = load('scripts/machineLearning/knn_opti.joblib')
    df_dataprocess = df_dataprocess[model.feature_names_in_]
    prediction = model.predict(df_dataprocess)
    with st.spinner(text='In progress'):
        time.sleep(3)
        st.success('Done')
    if prediction == 0:
        st.write("D'apres notre étude ce patient n'a pas de prédispotions à une maladie cardiaque" )
    else:
        st.write("D'apres notre étude ce patient peut avoir des prédispotions à une maladie cardiaque" )
    #st.write(prediction)
    # st.dataframe(df_dataprocess, use_container_width=True)

res_form ={}
elementFormNames= {0:'R_heartDisease',1:'R_smoking',3:'R_AlcoholDrinking',2:'R_Stroke',3:'R_DiffWalking',4:'R_Sex',5:'SB_AgeCategory',
                   6:'SB_Race',7:'SB_Diabetic',8:'R_PhysicalActivity',9:'SB_GenHealth',10:'R_Asthma',11:'R_KidneyDisease',12:'R_SkinCancer',
                   13:'S_PhysicalHealth',14:'S_MentalHealth',15:'S_BMI'}
st.title('Medical assistant ')

form = st.form("my_form",clear_on_submit =True)


with st.form(key ='Form1'):
    st.session_state.R_smoking = st.radio("Smoking",( 'Yes', 'No')  ),
    st.session_state.R_AlcoholDrinking = st.radio("Alcohol drinking",( 'Yes', 'No')  ),
    st.session_state.R_Stroke = st.radio("Stroke",( 'Yes', 'No')  ),
    st.session_state.R_DiffWalking = st.radio("Walking difficulty",( 'Yes', 'No')  ),
    st.session_state.R_Sex = st.radio("Sex",('Female', 'Male')  ),
    st.session_state.SB_AgeCategory = st.selectbox("Age Category",('18-29', '30-39','40-49', '50-59', '60-69', '70-79', '80 or older')),
    st.session_state.SB_Race = st.selectbox("Race",( 'White', 'Black', 'Asian', 'American Indian/Alaskan Native', 'Other', 'Hispanic')),
    st.session_state.SB_Diabetic = st.selectbox("Diabetic",('Yes', 'No', 'No, borderline diabetes', 'Yes (during pregnancy)')),
    st.session_state.R_PhysicalActivity = st.radio("Physical activity",( 'Yes', 'No')  ),
    st.session_state.SB_GenHealth= st.selectbox("General health",('Very good', 'Fair', 'Good', 'Poor', 'Excellent')),
    st.session_state.R_Asthma = st.radio("Asthma",('Yes', 'No')  ),
    st.session_state.R_KidneyDisease = st.radio("Kidney disease",( 'Yes', 'No')  ),
    st.session_state.R_SkinCancer = st.radio("Skin cancer",('Yes', 'No')  ),
    st.session_state.S_PhysicalHealth = st.slider('Physical health', 0, 30, 15),
    st.session_state.S_MentalHealth = st.slider('Mental health', 0, 30, 15),
    st.session_state.S_BMI = st.slider('BMI', 1, 100, 50),
    st.session_state.S_Sleep = st.slider('Sleeptime', 1, 24, 8),
    sub = st.form_submit_button("Submit")
if sub:
    runStat()

