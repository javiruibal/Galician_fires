# Galician_fires

En Galicia en los últimos años se han registrado gran cantidad de incendios, es un tema que año tras año es noticia en todos los telediarios. Por ello el objetivo de este proyecto, además de dar visibilidad a la gran cantidad de incendios que hubo en los últimos años, es intentar ayudar a la prevención de incendios a partir de los datos obtenidos de todos los incendios registrados entre los años 2001 y 2015. 
Puesto que no podemos predecir el factor humano, intentaremos predecir, a partir de las condiciones meteorológicas registradas, crear un modelo que prediga la posibilidad de un incendio en los principales focos.
Adicionalmente, se ha realizado un estudio de la localización de las diferentes torres de control ubicadas en Galicia, y cual sería su distribución óptima en función de los incendios registrados dependiendo del número de torres. 

## Organización del repo 
### Memoria: 
Incendios en Galicia.pdf
### Notebooks:
1- Limpieza de datos: Limpieza del dataset principal de incendios y agregación de los datos de superficie forestal por municipio

2- Carga de datos: carga de los datos geográficos y climatológicos y generar nuestra tabla final. 

3- Predicción de incendios: Modelo de predicción de incendios
  
    3.1- Regresion Log
  
    3.2- XGBoost - Sin NaN

    3.3- XGBoost - Con NaN

    3.4- XGBoost_Provincia

4- Geolocalación de torres de control: Modelo K-means adaptado a distancias geodésicas.

### Front end 
Función app.py para la ejecución del fron-end. 


##  Datos 
Todos los datos y los notebooks de este proyecto están disponibles en el siguiente enlace:

https://drive.google.com/drive/folders/1ro8QAvZongYj6_D6m9lgCDMcEV2q-r7W?usp=sharing


## Ejecución del código

Para ejecutar los notebooks, entrar desde la terminal en la carpeta descargada en el enlace anterior y ejecutar jupyter-notebook. Evitad mover los diferentes archivos de su ubicación original ya que puede perjudicar la ejecución del código. 

Para ejecutar el front-end desde local vaya a la carpeta Front_end y ejecute el script app.py. En la terminal, ejecute "streamlit run app.py"

## Requisitos
Librerías necesarias.
Pandas, numpy, datetime, re, streamlit, matplotlib, seaborn, altair, folium, streamlit-folium, Figure, branca.element, sklearn, XGBoost, pylab, ibmlearn, geopy, shapely, SMOTE, xlrd, openpyxl
