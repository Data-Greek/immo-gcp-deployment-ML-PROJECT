# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 13:09:07 2020

@author: TBEL972
"""
## CHARGEMENT DES LIBRAIRIES
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64
from io import BytesIO
from xgboost import XGBRegressor
from PIL import Image
import xlsxwriter


## Chargement du modèle (joblib)
model = joblib.load('immo_model.pkl')

## Fonction de prédiction
def predict(input_df):
    prediction = model.predict(input_df)
    return prediction

## CRÉATION DE L'APPLICATION
def app():
    
    ## En-tête
    html_template = """
    <div style = "background-color : #6495ED ; padding:15px">
    <h2 style="color : white; text-align : center; ">Estimateur du prix de l'immobilier</h2>
    
    """
    st.markdown(html_template, unsafe_allow_html=True)
    
    st.write("")
    
    #st.header("Estimateur de prix de bien foncier pour le compte d'agence immobilière") 
    st.write(" Cet outil de démonstration se base sur un jeu de donnée ayant permis la création d'une interface de calcul en temps réel visant à estimer les prix de biens immobiliers afin de les acquérir ou les vendre au juste prix, et anticiper leur valorisation sur le marché.")
             
    ## Création la sidebar
    sidebar_selection = st.sidebar.selectbox("Type de prédiction", ("Prédiction en temps réel", "Prédiction par lot (batch)"))
    
    ## Personnalisation de la sidebar
    
    st.sidebar.info("Cette application est une démonstration, conçue par la team data science de l'**Agence Marketic**")
    
    st.sidebar.success('Vous souhaitez concevoir **votre propre interface de prédiction**, adaptée aux réalités de votre terrain/de votre public ? Alors, retrouvez-nous sur **http://www.agence-marketic.fr**')
    
    image = Image.open('real_estate.jpg')
    
    st.sidebar.image(image, use_column_width=True)
    
    ## PREDICTION EN TEMPS REEL
    
    if sidebar_selection == "Prédiction en temps réel":
        
        st.write("Veuillez renseigner les paramètres suivants afin d'obtenir une estimation de l'intelligence artificielle pour le prix du bien que vous souhaitez estimer 🏠.")
        
        anciennete = st.number_input("Ancienneté du bien immobilier", min_value=1, max_value=100, value=34)
        nombre_pieces	= st.number_input("Nombre de pièces", min_value=1, max_value=15, value=2)
        nombre_chambres = st.number_input("Nombre de chambres ", min_value=1, max_value=15, value=3)
        population_en_millier = st.text_input("Nombre d'habitants de la localité où est implanté le bien foncier", "20000")
        nombre_foyer = st.text_input("Nombre de foyers résidant dans la localité où est vendu le bien foncier ", "4000")
        revenue_moyen_habitants = st.text_input(" Revenu moyen des résidents de la localité ", "25000")
        proximite_mer = st.selectbox("Le bien immobilier se situe : ",["Non loin des côtes", "A l'interieur des terres", "En bord de mer", "Dans une marina"])
       
       ## création d'un dictionnaire + dataframe
       
       
        data = {'anciennete' : anciennete, 
               'nombre_pieces':nombre_pieces,
               'nombre_chambres':nombre_chambres,
               'population_en_millier':population_en_millier,
               'nombre_foyer':nombre_foyer,
               'revenue_moyen_habitants':revenue_moyen_habitants,
               'proximite_mer':proximite_mer
               }
       
       
        input_df = pd.DataFrame(data, index=[0])
       
        resultat = ""
    
        if st.button("Prédiction"):
        
            resultat = model.predict(input_df)
            st.success("Le bien foncier est estimé à **{}€**".format(resultat))
            
        
        
    ## TRAITEMENT PAR LOT
    
    if sidebar_selection == "Prédiction par lot (batch)":
        
        st.write("""Pour servir de démonstration, veuillez télécharger puis charger le fichier ci-dessous, afin d'obtenir une estimation par lot de l'intelligence artificielle pour le prix du bien que vous souhaitez estimer 🏠.""")
        
        demo = st.markdown("""[1️ - Télécharger le fichier de démonstration](https://drive.google.com/uc?export=download&id=1C0x6Gb9ieIsVArz29ci5dW8ekOuz7_02) ✅""")
        batch = st.file_uploader("Insérez le fichier de démonstration en cliquant sur ''browse files''", type="csv")
        
        ## génération de la prédiction
        if batch is not None:
            df = pd.read_csv(batch)
            prediction = model.predict(df)
            
            ## mise en forme
            pred = pd.Series(prediction.reshape(df.shape[0],))
            concat = pd.concat([df,pred], axis=1)
            concat.columns = ['anciennete','nombre_pieces','nombre_chambres','population_en_millier','nombre_foyer','revenue_moyen_habitants','proximite_mer', 'Prediction']
            final = st.write(concat)
            
            ## Télécharger le fichier de prédiction
            st.write("")
            st.write("2 - Télécharger le fichier de prédiction ⬇️")
            

            def to_excel(concat):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                concat.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                processed_data = output.getvalue()
                return processed_data

            def get_table_download_link(concat):
                val = to_excel(concat)
                b64 = base64.b64encode(val)
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Prédictions_Agence Marketic.xlsx">Lancer le téléchargement</a>' 

           
            st.markdown(get_table_download_link(concat), unsafe_allow_html=True)
        
if __name__=='__main__':
    app()
