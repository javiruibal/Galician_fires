import streamlit as st
from PIL import Image
import pandas as pd
import streamlit.components.v1 as components
import folium
from folium.raster_layers import WmsTileLayer
from folium.raster_layers import TileLayer
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
from branca.element import Figure

def app():
    
    #Título de la página
    st.title('Geolocalización de torres de control')

    st.write('Basándonos en el modelo K-Means adaptado a distancias geodésicas, a continuación se muestran las localizaciones óptimas de las torres de control en función de las distancias a los focos de incendios ocurridos entre los años 2001 y 2015')

    
    ## Sidebar - Number of coins to display
    num_torres = st.slider('Número de torres de control', 40, 50, 44)    
    
    #Dividimos la pagina en dos columnas 
    col1, col2 = st.beta_columns((1,1.5))
        
    col1.header('Localización de las actuales torres de control')
    col1.write('44 torres de control')
    
    image = Image.open('Torres de control.PNG')

    col1.image(image, width = 555)
    
    col2.header('Visualización del modelo K-Means')
    col2.write(str(num_torres) + ' torres de control')
    
    Htmlfile=open(str(num_torres) +'Torres.html','r',encoding='utf-8')
    source_code=Htmlfile.read()
    with col2:
        components.html(source_code, height=560)

        
   
 