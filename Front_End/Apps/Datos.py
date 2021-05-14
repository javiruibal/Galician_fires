import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import folium_static
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import folium
import pandas as pd
import numpy as np
from folium.raster_layers import WmsTileLayer
from folium.raster_layers import TileLayer
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
from branca.element import Figure
import seaborn as sns
import altair as alt


def app():
    st.write("""---""")
    st.title('Datos')

    #---------------------------------#
    #st.set_page_config(layout="wide")
    #---------------------------------#
    
    ## Dividir la página en 3 columnas
    col1 = st.sidebar
    col2, col3 = st.beta_columns((0.9,1))

    #---------------------------------#
    # Sidebar 
    col1.header('Parámetros de entrada')

    ## Sidebar - Filtro del Año
    year = col1.selectbox('Año', list(reversed(range(2001,2016))))

    # Carga de datos
    #@st.cache
    df=pd.read_csv('datos_rios_embalses_tiempo.csv', index_col=[0])
    

    ## Sidebar - Provincia
    provincias = sorted( df['provincia'].unique() )
    selected_provincias = col1.multiselect('Provincias', provincias, provincias)
    
    ##Filtra el data frame
    
    df_filtered = df[(df['ano']==year) & (df['provincia'].isin(selected_provincias))]
    df_filtered_show = df_filtered[['id', 'superficie', 'fecha_x', 'lat', 'lng', 'idprovincia',
       'idmunicipio', 'municipio_x', 'time_ctrl', 'time_ext', 'personal',
       'medios', 'gastos', 'perdidas', 'codigo', 'superficie_total_concello',
       'superficie_forestal_total', 'nombre', 'río', 'capacidad_emb',
       'sup_emb', 'lat_embalse', 'lng_embalse', 'dist_emb_x',
       'num_rios', 'provincia', 'estación',
       'latitud', 'longitud', 'temp_media', 'temp_max_med', 'temp_min_med',
       'prec_acu', 'hum_med', 'hum_max', 'hum_min', 'v_viento_med', 'presion',
       'lluvia', 'helada', 'dist_est_x']]
    df_filtered_desc = df_filtered[['superficie','time_ctrl', 'time_ext', 'personal',
       'medios', 'gastos', 'perdidas', 'superficie_total_concello',
       'superficie_forestal_total', 'capacidad_emb','sup_emb', 'dist_emb_x',
       'num_rios', 'provincia', 'estación','temp_media', 'temp_max_med', 'temp_min_med',
       'prec_acu', 'hum_med', 'hum_max', 'hum_min', 'v_viento_med', 'presion',
       'lluvia', 'helada', 'dist_est_x']]
    

    #---------------------------------#
    # Resumen estadistico de las variables 
    col2.subheader('Descripción estadística')
    col2.write('Entre los primeros pasos de todo análisis de datos se encuentra la descripción estadistica de las variables en estudio. En esta fase se pueden observar los principales parámetros de centralización, dispersión y posición, con ellos se resume a alto nivel el comportamiento de las variables en cuestión.')
    col2.write(df_filtered_desc.describe())
    
    # total de incendios
    col3.subheader('Número total de incendios')
    if len(selected_provincias)== 4:
        range_=["#808000","#FF6F00","#CD853F","#800000"]
    elif len(selected_provincias)== 3:
        range_=["#808000","#CD853F","#800000"]
    elif len(selected_provincias)== 2:
        range_=["#808000","#CD853F"]
    else:
        range_=["#808000"]
            
    inc_line=alt.Chart(df_filtered).mark_line().encode(
    x="num_mes",
    y="count(id)",
    color=alt.Color('provincia',scale=alt.Scale(range=range_)))
    inc_bar=alt.Chart(df_filtered).mark_bar().encode(
    x="provincia",
    y="count(id)",
    color=alt.Color('provincia',scale=alt.Scale(range=range_)))
    inc_tot=inc_bar|inc_line
    col3.write(inc_tot)
    
    
    # Superficie quemada
    def Q1(x):
        return x.quantile(0.25)
    def Q2(x):
        return x.quantile(0.5)
    def Q3(x):
        return x.quantile(0.75)
    sns.set(style='white',rc={"font.size":12,"axes.labelsize":12,"axes.titlesize":12,"font.family":"serif"})
    if len(selected_provincias)> 2:
        st.subheader('Descripción estadística de superficie quemada')
        st.markdown("""A continuación se muestran los principales parámetros descriptivos enfocados en la superficie quemada (*ha*) por las provincias seleccionas:""")
        st.write(df_filtered.groupby(['provincia']).agg({'superficie': ['sum','mean','min',Q1,Q2,Q3,'max','std']}))

        st.subheader('Superficie quemada por mes')
        st.pyplot(sns.relplot(data=df_filtered, x='num_mes',y='superficie',kind='line', hue='provincia',col='provincia', palette=range_, height=3.5))
    elif len(selected_provincias)== 2:
        col2.write(' ')
        col2.write(' ')
        col2.write(' ')
        col2.write(' ')
        col2.subheader('Descripción estadística de superficie quemada')
        col2.markdown("""A continuación se muestran los principales parámetros descriptivos enfocados en la superficie quemada (*ha*) por las provincias seleccionas:""")
        col2.write(df_filtered.groupby(['provincia']).agg({'superficie': ['sum','mean','min',Q1,Q2,Q3,'max','std']}))

        col3.subheader('Superficie quemada por mes')
        col3.pyplot(sns.relplot(data=df_filtered, x='num_mes',y='superficie',kind='line', hue='provincia',col='provincia', palette=range_, height=3.5))
    else:
        col2, col3 = st.beta_columns((2,1))
        col2.write(' ')
        col2.write(' ')
        col2.subheader('Descripción estadística de superficie quemada')
        col2.markdown("""A continuación se muestran los principales parámetros descriptivos enfocados en la superficie quemada (*ha*) por las provincias seleccionas:""")
        col2.write(df_filtered.groupby(['provincia']).agg({'superficie': ['sum','mean','min',Q1,Q2,Q3,'max','std']}))
        sns.set(style='white',rc={"font.size":2,"axes.labelsize":2,"axes.titlesize":2,"xtick.labelsize":2,"ytick.labelsize":2,"legend.fontsize":2,"legend.title_fontsize":2,"font.family":"serif","lines.linewidth":0.5})
        col3.subheader('Superficie quemada por mes')
        col3.pyplot(sns.relplot(data=df_filtered, x='num_mes',y='superficie',kind='line', hue='provincia',col='provincia', palette=range_, height=3))
    #-------------
    st.subheader('Datos de incendios')
    st.write('Dimensiones: ' + str(df_filtered_show.shape[0]) + ' filas y ' + str(df_filtered_show.shape[1]) + ' columnas.')

    st.write(df_filtered_show)

    # Descargar CSV data
    @st.cache
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode() 
        href = f'<a href="data:file/csv;base64,{b64}" download="incendios_galicia.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(df_filtered_show), unsafe_allow_html=True)
    #---------------------------------#
    # Mapa de incendios
    st.subheader('Evolución de incendios')
    
    meses= df_filtered['num_mes'].unique()
    meses.sort()
    
    lat_lng_list= []
    for i in meses:
        temp=[]
        for index, instance in df_filtered[df_filtered['num_mes']==i].iterrows():
            temp.append([instance['lat'], instance['lng']])
        lat_lng_list.append(temp)

    EsriImagery = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    EsriAttribution = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"

    figure1=Figure(width=550, height=700)
    MapObject = folium.Map(location=[42.65, -7.84], tiles=EsriImagery, attr=EsriAttribution, zoom_start=8)

    Mapa=figure1.add_child(MapObject)
    HeatMapWithTime(lat_lng_list, radius=12,  gradient={.2: '#fffacd', .5: '#ffd700', 1: '#ff0000' }, position='bottomright').add_to(MapObject)
    #col3.MapObject
    MapObject.save('mapa_dinamico_incendios_galicia.html')
    
   
    #figure2=folium.Figure(width=550,height=550)
    #MapObject = folium.Map(location=[42.733581, -7.838777], tiles=EsriImagery, attr=EsriAttribution, zoom_start=8)
    #HeatMap(list(zip(df_filtered[df_filtered['num_mes']=='12']['lat'],df_filtered[df_filtered['num_mes']=='12']['lng'])), radius=12,  gradient={.2: '#fffacd', .5: '#ffd700', 1: '#ff0000' }).add_to(MapObject)
    
    #m = figure2.add_child(MapObject)
    #m.save('mapa_incendios_galicia.html')
    #col3.write(""" Mapa de los incidenosde mes de Diciembre """)
    #col3.write(components.html(figure2._repr_html_(),height=560))
    Htmlfile=open('mapa_dinamico_incendios_galicia.html','r',encoding='utf-8')
    source_code=Htmlfile.read()
    components.html(source_code, height=560)
    