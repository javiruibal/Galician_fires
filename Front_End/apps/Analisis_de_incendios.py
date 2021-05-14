import streamlit as st
import numpy as np
import pandas as pd
import pickle
import xgboost
from sklearn import datasets
from math import radians, cos, sin, asin, sqrt


def app():


    # Carga de datos
    #@st.cache
    pueblos = pd.read_csv('coordenadas_municipios.csv', index_col=[0])
    estaciones=pd.read_excel('tiempo_actual.xlsx')
    estaciones.columns = map(lambda x: str(x).lower(), estaciones.columns) 
    estaciones['provincia'] = estaciones['provincia'].str.upper()
    estaciones['idprovincia'] = estaciones['provincia'].apply(lambda x: 15 if x=='A CORUÑA' else (32 if x=='OURENSE' else (27 if x=='LUGO' else 36)))


    #Cargamos funcion distancias 
    def distance(lat1, lat2, lon1, lon2): 

        # radians which converts from degrees to radians. 
        lon1 = radians(lon1) 
        lon2 = radians(lon2) 
        lat1 = radians(lat1) 
        lat2 = radians(lat2) 

        # Haversine formula  
        dlon = lon2 - lon1  
        dlat = lat2 - lat1 
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

        c = 2 * asin(sqrt(a))  

        # Radius of earth in kilometers. Use 3956 for miles 
        r = 6371

        # calculate the result 
        return(c * r) 
    @st.cache
    def dist_min(df1,column_lat1,column_lat2,column_lng1,column_lng2,index,name):
    
        #Add column containing distances 
        df1[name]=df1.apply(lambda x: distance(x[column_lat1], x[column_lat2], x[column_lng1], x[column_lng2]), axis=1)
        #Selecting the min distance per id
        df1_min = df1.groupby([index]).agg({name: 'min'})
        df2 = pd.merge(df1, df1_min, on = index, how ='inner')
        df = df2[(df2[name+'_x']==df2[name+'_y']) | df2[name+'_x'].isna()]
        return(df)
    

    def join(df1, df2):
        df_join = pd.merge(df1, df2, on = ['idprovincia'], how ='inner')

        df_join = dist_min(df_join, 'latitud_x', 'latitud_y', 'longitud_x', 'longitud_y', 'población','distancia_pueblo')

        return df_join
    
    
    #---------------------------------#
    #st.set_page_config(layout="wide")
    #---------------------------------#
    
    st.title('Análisis de Incendios')
    st.header('Predicción de la probabilidad de incendio según los datos climatológicos')

    st.write('En esta sección se predice la probabilidad de incendio de los municipios de Galicia en función de los datos climatológicos correspondientes a la estación meteorológica más próxima.')    
    
    col1, col2 = st.beta_columns((1,1))

    provincias=pueblos['provincia'].unique()
    
    prov = col1.selectbox('Provincia', list(provincias))
    pueblo = col2.selectbox('Municipio', list(pueblos[pueblos['provincia']==prov]['población']))
    
    resultados = join(pueblos[(pueblos['población']==pueblo) & (pueblos['provincia']==prov)], estaciones[estaciones['provincia']==prov])
    
    resul_x = resultados[['temp_media','temp_max_med','temp_min_med','prec_acu','hum_med','hum_max','hum_min','v_viento_med','presion','lluvia','helada']]
    
    st.markdown(""" **Estación meteorológica**:  """)
    st.write(resultados['estación'])
    
    st.markdown(""" **Datos climatológicos**:  """)
    st.write(resul_x)
    
 
    st.markdown(' <span style="font-size:0.8em;">Unidades de medida de los datos: Temperatura: *ºC*; Precipitación acumulada: *l/m²*; Humedad relativa: *%*;  Velocidad del viento: *km/h*;   Presión: *hPa*;   lluvia: *días*;  helada: *días*.</span>', unsafe_allow_html=True)

    #Carga de los modelos 
    if prov=='A CORUÑA':
        clf = pickle.load(open('model_15.sav','rb'))
    elif prov=='LUGO':
        clf = pickle.load(open('model_27.sav','rb'))
    elif prov=='OURENSE':
        clf = pickle.load(open('model_32.sav','rb'))
    else:
        clf = pickle.load(open('model_36.sav','rb'))

    prob =  clf.predict_proba(resul_x)[:,1][0]
    
    st.markdown(""" **Probabilidad de incendio**:  """)
    st.write(str(round(prob*100,2))+' %')
    
    