import streamlit as st
from multiapp import MultiApp
#Import pestañas
from apps import Datos ,Geolocalizacion_torres_de_control , Analisis_de_incendios  

app = MultiApp()
## Page expands to full width
st.set_page_config(layout="wide") 
st.title("Incendios en Galicia")
st.markdown("""
En comparación con el resto de España, Galicia es una de las comunidades más afectadas por los incendios producidos cada año. Este hecho fuerza numerosos estudios y análisis con el objetivo tanto de prevenir el mayor número de incendios como optimizar los recursos utilizados para su extinción
""")
#---------------------------------#
# Información de interés
expander_bar = st.beta_expander("Información de interés")
expander_bar.markdown("""
- **Librerías de Python:** pandas, numpy, datetime, re, streamlit, matplotlib, folium, Figure, KMeans, seaborn, sklearn, xgboost, pylab, imblearn.
- **Fuente de datos:** 
    * [Instituto geografico nacional](https://www.ign.es/web/ign/portal/ane-datos-geograficos/-/datos-geograficos/datosHidro?tipo=embalses&provincia=todas).
    * [Meteogalicia] (https://www.meteogalicia.gal/observacion/informesclima/informesIndex.action?request_locale=gl).
    * [PLADIGA] (https://mediorural.xunta.gal/es/temas/defensa-monte/pladiga-2020).
""")
#---------------------------------#
# Añadir las pestañas
app.add_app("Datos", Datos.app)
app.add_app("Análisis de incendios", Analisis_de_incendios.app)
app.add_app("Geolocalización de torres de control", Geolocalizacion_torres_de_control.app)
# The main app
app.run()