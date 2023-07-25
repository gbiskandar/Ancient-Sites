#Importamos librerias necesarias
import streamlit as st
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt


# Titulo del EDA
st.header("Exploratory Data Analysis (EDA)")
st.subheader("by Guillermo Bogran")
st.write("Web Scraping de datos sobre Sitios Antiguos del Mundo y realización de analisis y visualización de los datos obtenidos. Tecnologias utilizados incluyen, pero no limitadas, a: Python scripting language, beautiful soup library, pandas, matplotlib, folium, gensim, APIs y StreamLit.")

st.write("\n")
st.write("\n")

# Introduccion
st.subheader("Inicio: WebScraping")
st.write("Para el proposito del EDA, encontré el siguiente sitio web con url: http://www.ancient-wisdom.com/megalithicdatabase.htm que contiene informacion sobre monumentos Prehistóricos y Sagrados alrededor del mundo.")

# Imagenes
img4 = 'utils/img/ancient-wisdom-homepage.png'    
img5 = 'utils/img/ancient-wisdom-table.png' 
img6 = 'utils/img/ancient-wisdom-abu-simbel.png' 


st.expander('Expander')
with st.expander('Imagenes del sitio web: Ancient Wisdom'):
    st.image(img4, caption="Homepage")
    st.image(img5, caption="Tabla de Contenidos")

# Scrapear la tabla de Contenidos
st.write("")
st.write("Iniciamos scraping la Tabla De Contenidos con el nombre de cada Sitio Antiguo y tambien obtenemos el link hacia la pagina única de cada sitio.")
with st.expander('Codigo de Scraping la Tabla de Contenidos'):
    code = """
        # importamos librerias
        from bs4 import BeautifulSoup as bs
        import requests
        import pandas as pd
        import numpy as np

        url = "http://www.ancient-wisdom.com/no-searching/azlocations.htm"
        r = requests.get(url)
        soup = bs(r.content, 'lxml')

        data = []

        # identificamos cada registro con la variable address
        address = soup.findAll('address', {'align':'left'})

        # Scraping de Nombre de los Sitios en la tabla
        n = np.arange(200) 
        lista_lugares = [] # Crear una lista para guardar los nombres
        for i in n:
            try:
                place = address[i].find('font').get_text().replace('.','').replace('\n','').replace('\t','').strip() # Identificar cada lugar y limpiar lo que se scrap
                lista_lugares.append(place) #incluir en la lista correspondiente
            except:
                lista_lugares.append(np.NaN) # si viene vacío, incluir un NaN  
                None

        # Scraping de los Tipos de Sitios
        lista_tipo = [] # Crear una lista para guardar los tipos de Sitios
        for i in n:
            try:
                site_type = address[i].find('font',{'size': '1'}).get_text(strip=True).replace('(','').replace(')','').replace('\n','').replace('\t','').replace('.','') # Identificar por atributo de size = 1 y limpiar lo que se scrap
                lista_tipo.append(site_type)
            except:
                lista_tipo.append(np.NaN)   
                None

        # Scraping de los links 
        lista_links = [] # Crear una lista para guardar los links de los Sitios
        for i in n:
            try:
                url_principal = 'http://www.ancient-wisdom.com/'
                short_url = address[i].find('a').get('href') # Identificar mediante <a href>
                lista_links.append(url_principal+short_url[3:]) # Limpiar obviando los primeros 3 char y crear el url largo
            except:
                lista_links.append(np.NaN)   
                None

        # Creamos el DataFrame inicial
        df = pd.DataFrame()
        df['sitios']=lista_lugares
        df['tipo']=lista_tipo
        df['url']=lista_links
        """
    st.code(code, language='python')     

# Cada Sitio Antiguo tiene un url donde contiene mayor informacion sobre el sitio

st.write("Cada Sitio Antiguo en Ancient Wisdom tiene su propia pagina web, la cual debemos web scrap tambien.")
st.expander('Expander')
with st.expander('Imagen muestra de la pagina web de cada sitio'):
    st.image(img6, caption="Pagina Web: Abu Simbel, Egypt")
with st.expander('Codigo de Scraping las Paginas Web de cada Sitio'):
    st.echo()
    code = """
        # importamos librerias
        from bs4 import BeautifulSoup as bs
        import requests
        import pandas as pd
        import numpy as np

        #Scraping del texto del sitio en cada link 
        lista_textos = [] # Creamos una lista donde guardar el texto
        for i in range(len(lista_links)): # haciendo uso de la lista creada previamente lista_links 
            try:
                url = lista_links[i]
                r = requests.get(url)   
                soup = bs(r.content, 'lxml')
                
                all_p = soup.find_all('p' , align='justify') # identificamos los parrafos a scrap
                
                count = 1
                full_text = "" # creamos una variable full text donde se iran agregando
                for i in all_p:
                    print(count , '\n')
                    print(i.get_text(strip=True) , '\n')
                    p_text = i.get_text(strip=True) + ' '  # guardamos el texto del parrafo en p_text
                    full_text += p_text # se va acumulando todos los textos de cada parrafo en full_text
                    count += 1
                print(full_text)
                lista_textos.append(full_text) # se incluye el full_text de cada sitio en la lista
            except:
                lista_textos.append(np.NaN)   
                None
            
            lista_info = []
            for i in range(len(lista_textos)):
                try:
                    lista_textos[i] = lista_textos[i].replace('\n','').replace('\t','') # limpiar el texto de lineas nuevas y tabulaciones
                    lista_textos[i] = lista_textos[i].replace('         ',' ').replace('     ',' ') # limpiar el texto de espacio en blanco
                    lista_info.append(lista_textos[i])
                except:
                    lista_info.append(np.NaN)
                    None

            # Scraping del texto del titulo del sitio en cada link 
            lista_titulos = []
            for i in range(len(lista_links)):
                try:
                    url = lista_links[i]
                    r = requests.get(url)   
                    soup = bs(r.content, 'lxml')
                    
                    titulo = soup.title.text.replace('.','')  # limpiar el texto de los titulos      
                    lista_titulos.append(titulo)
                except:
                    lista_titulos.append(np.NaN)
                    None

            # Agregar titulos e información al dataframe 
            df['titulos']=lista_titulos
            df['informacion']=lista_info

            # Creamos un dataframe llamado ancient
            ancient = df.dropna(thresh=2) # Droppeamos las filas con mas de 2 NaN, es decir que son encabezados o no se scrap bien

        """
    st.code(code, language='python')

# Conseguir Coordenadas para los Sitios

st.subheader("Uso de APIs y manipulacion de datos")
st.write("Nos interesan las coordendas de cada sitio, para poder plot en un mapa. Por lo tanto usaremos el GoogleMaps API para la obtención de coordenadas. Adicionalmente, queremos conseguir un resumen de la informacion de cada sitio para reducir la cantidad de texto y resaltar información importante")
st.expander('Expander')
with st.expander('Codigo de Obtencion y Limpieza de Coordenadas'):
    st.echo()
    code = """
        # Importamos librerias
        import googlemaps
        import numpy as np
        import pandas as pd
        from datetime import datetime

        gmaps = googlemaps.Client(key=[INSERT API KEY HERE]) # utiliza tu propia API key en esta linea

        sitios_list = ancient.sitios.values.tolist()
        coord_list = [] # Crea una lista donde guardar las coordenadas de cada sitio

        for i in range(len(sitios_list)):
                try:
                    reverse_geocode_result = gmaps.geocode(sitios_list[i]) # Nombre de cada Sitio en la lista
                    coord = tuple(reverse_geocode_result[0]['geometry']['location'].values())
                    coord_list.append(coord)
                except:
                    coord_list.append(np.NaN)  
        print(coord_list)

        # Separar coordenadas de sitios en LAT y LONG

        latitude_list = [] # lista de latitudes
        longitude_list = [] # lista de longitudes

        for i in range(len(coord_list)):
            try:
                latitude = coord_list[i][0]
                longitude = coord_list[i][1]
                latitude_list.append(latitude)
                longitude_list.append(longitude)
            except:
                latitude_list.append(np.NaN)
                longitude_list.append(np.NaN)

        # Agregar Columna de Coordenadas para ancient df
        ancient['coord']=coord_list

        # Agregar Columna de LAT y LONG para ancient df
        ancient['latitude']=latitude_list
        ancient['longitude']=longitude_list

        # Crear un csv de ancient df
        ancient.to_csv('ancient_data.csv', index=False) 

        """
    st.code(code, language='python')

# Resumir el texto completo de la pagina web en una nueva columna de resumen

st.expander('Expander')
with st.expander('Codigo de Resumen Extractivo'):
    st.echo()
    code = """
        # Importamos librerias
        %pip install gensim==3.8
        from gensim.summarization import summarize

        def extractive_summarize(text):
            # Revisar si el texto es un string
            if isinstance(text, str):
                # Aplicar la funcion gensim de resumir
                resumen = summarize(text, ratio=0.3) # resumen tiende a ser 30% del texto original
                if resumen == '':
                    # Si la funcion gensim no lo pudo resumir, toma las primeras 2 sentencias
                    sentences = text.split('. ')
                    resumen = '. '.join(sentences[:2]) + '.'
            else:
                # Si el texto no es string (i.e. NaN), el resumen sera un string vacio
                resumen = ''
            
            return resumen

        # Aplicar la funcion de resumir gensim a la columna 'informacion'
        ancient['resumen'] = ancient['informacion'].apply(extractive_summarize)

        # Guardar el df a un nuevo archivo csv
        ancient.to_csv('ancient_data_con_resumen.csv', index=False) 

        """
    st.code(code, language='python')

st.expander('Expander')
with st.expander('Codigo de Data Clean-Up: Pais'):
    st.echo()
    code = """
        # Extraer informacion de pais de la columna 'sitios'
        ancient['pais'] = ancient['sitios'].apply(lambda x: x.split(",")[-1].strip())

        # Conseguir el numero de paises unicos
        paises_unicos = ancient['pais'].unique()

        # Funcion para limpiar los nombres de los paises
        def limpiar_nombre_pais(pais):
            if '(' in pais:
                return pais.split('(')[0].strip()
            elif pais in ['Pacific', 'Africa', 'C', '']: # Nombres que no son de paises
                return 'Unknown'
            elif pais == 'Salisbury Complex':
                return 'United Kingdom'
            else:
                return pais

        # Aplicar la funcion a la columna 'country'
        ancient['pais'] = ancient['pais'].apply(limpiar_nombre_pais)

        # Guardar paises unicos ya limpio
        paises_limpios_unicos = ancient['pais'].unique()

        # Registros que no son paises
        registro_no_pais = ['Circle)', 'Flattened Hilltop)', 'Er-Grah', 'Gors Fawr', 'Bugibba']

        # Marcar registros que no son paises como Desconocidos
        ancient['pais'] = ancient['pais'].apply(lambda x: 'Unknown' if x in registro_no_pais else x)
        """
    st.code(code, language='python')

st.expander('Expander')
with st.expander('Codigo de Data Clean-Up: Continente'):
    st.echo()
    code = """
        pais_a_continente = {
            'Egypt': 'Africa',
            'Ethiopia': 'Africa',
            'Armenia': 'Asia',
            'China': 'Asia',
            'Iran': 'Asia',
            'Iraq': 'Asia',
            'Lebanon': 'Asia',
            'Pakistan': 'Asia',
            'Russia': 'Asia',
            'Turkey': 'Asia',
            'Belgium': 'Europe',
            'England': 'Europe',
            'France': 'Europe',
            'Germany': 'Europe',
            'Greece': 'Europe',
            'Ireland': 'Europe',
            'Italy': 'Europe',
            'Malta': 'Europe',
            'Portugal': 'Europe',
            'Scotland': 'Europe',
            'Serbia': 'Europe',
            'Spain': 'Europe',
            'Wales': 'Europe',
            'United Kingdom': 'Europe',
            'Mexico': 'North America',
            'Guatemala': 'North America',
            'USA': 'North America',
            'New Mexico': 'North America',
            'Bolivia': 'South America',
            'Chile': 'South America',
            'Colombia': 'South America',
            'Peru': 'South America',
            'Easter Island': 'Oceania',
            'Unknown': 'Unknown'
        }

        # Agregar una nueva columna al dataframe de continente
        ancient['continente'] = ancient['pais'].map(pais_a_continente)

        # Guardar el df a un nuevo archivo csv
        ancient.to_csv('ancient_data_paises.csv', index=False)

        """
    st.code(code, language='python')    

# La elaboración del dataframe inicial 'ancient' ha sido realizada.

st.write("Nuestro dataframe 'ancient' ha sido finalizado. Incluye: El nombre de los sitios, tipo, url, titulo, informacion completa de la página web, coordenadas (LAT y LONG), pais, continente, y un resumen de la información de cada pagina web. Finalmente, los datos estan organizados y limpios.")

# Cargar el dataframe a StreamLit
data = pd.read_csv('data/ancient_data_paises.csv')

# Mostrar el DataFrame
st.subheader('Mostramos el Dataframe: Ancient Data')
st.write(data)

# Data Analysis
st.subheader("Análisis de Datos")

# Creamos el plot de Distribucion de Tipo de Sitios
st.write('Nos interesa saber sobre la Distribucion de Tipo de Sitios')
st.expander('Expander')
with st.expander('Creamos el plot de Distribucion de Tipo de Sitios'):
    st.echo()
    with st.echo():
        site_type_counts = data['tipo'].value_counts()
        top_20_site_types = site_type_counts[:20]
        fig1, ax1 = plt.subplots()
        top_20_site_types.plot(kind='barh', color='skyblue', ax=ax1)
        ax1.set_title('Distribucion de Tipo de Sitios')
        ax1.set_xlabel('Count')
        ax1.set_ylabel('Tipo de Sitio')
        ax1.invert_yaxis()
    
# Mostramos el Plot de Distribucion de Tipo de Sitios
st.write('Mostramos el plot')
with st.echo():
    st.pyplot(fig1)

# Imagenes de los top 3 tipos de Sitios
img1 = 'utils/img/dolmen.jpg'    
img2 = 'utils/img/passage-mound.jpeg'
img3 = 'utils/img/stone-circle.jpeg'

st.expander('Expander')
with st.expander('Imagenes de Top 3 - Tipo de Sitios'):
    st.image(img1, caption="Dolmen")
    st.image(img2, caption="Passage Mound")
    st.image(img3, caption="Stone Circle")



# Crear el mapa de sitios usando Folium
st.write('Nos interesa saber donde estan ubicados los Sitios Antiguos en el mapa')
st.expander('Expander')
with st.expander('Creamos el mapa de sitios usando Folium'):
    st.echo()
    code = """
        mapa = folium.Map(location=[0, 0], zoom_start=2)

        for index, row in data.iterrows():
            try:
                folium.Marker(location=[row['latitude'], row['longitude']], 
                popup=row['tipo'],
                tooltip=row['sitios']).add_to(mapa)
            except:
                None"""
    st.code(code, language='python')            

path_to_html = "utils/html/mapa_sitios_antiguos.html"
# Leer el archivo y guardarlo en una variable
with open(path_to_html,'r') as f: 
    html_data = f.read() 
# Mostrarlo en StreamLit
st.subheader("Sitios Antiguos del Mundo")
st.components.v1.html(html_data,height=500)

# Creamos el Grafico de los Paises
st.write('Nos interesa saber sobre la Distribucion de Paises de los Sitios')
st.expander('Expander')
with st.expander('Creamos el plot de Distribucion de Sitios por Pais'):
    st.echo()
    with st.echo():
        # Contar el numero de sitios por pais
        pais_counts = data['pais'].value_counts()

        # Mostrar un bar graph
        fig2, ax2 = plt.subplots()
        pais_counts.sort_values().plot(kind='barh', color='skyblue')
        ax2.set_xlabel('Numero de Sitios')
        ax2.set_ylabel('Pais')
        ax2.set_title('Numero de Sitios Antiguos por Pais')
    
# Mostramos el Plot de Distribucion de Sitios por Pais
st.write('Mostramos el plot')
with st.echo():
    st.pyplot(fig2)

# Creamos el Grafico de los Continentes
st.write('Nos interesa saber sobre la Distribucion de Paises por Continentes')
st.expander('Expander')
with st.expander('Creamos el plot de Distribucion de Sitios por Continente'):
    st.echo()
    with st.echo():
        # Contar el numero de sitios por pais
        continente_counts = data['continente'].value_counts()

        # Mostrar un bar graph
        fig3, ax3 = plt.subplots()
        continente_counts.sort_values().plot(kind='barh', color='skyblue')
        ax3.set_xlabel('Numero de Sitios')
        ax3.set_ylabel('Continente')
        ax3.set_title('Numero de Sitios Antiguos por Continente')
    
# Mostramos el Plot de Distribucion de Sitios por Pais
st.write('Mostramos el plot')
with st.echo():
    st.pyplot(fig3) 

# Mostramos el Plot de Distribucion de Sitios por Pais
st.header('Conclusiones')
st.write("Una ves realizada la investigación podemos llegar a las siguientes conclusiones:")
st.write("-  La distribución de sitios antiguos es de alcance global")
st.write("-  Existe un claro sesgo a los sitios antiguos ubicados en Europa")
st.write("-  Las estructuras monoliticas de piedra para usos fúnebres o astronomía predominan en la antigüedad")

# Siguientes Pasos
st.subheader('Oportunidades')
st.write("- Analisis NLP sobre la informacion de cada sitio y su resumen. Que tienen en comun los sitios antiguos? Que información es la que mas sobresale?")
st.write("- Ahora que se empezó una base de datos de sitios antiguos, posiblemente turísticos. Averiguar si hay un mercado para viajes turísticos, de investigacion, etc.")
st.write("- Incrementar la cantidad de Sitios, scraping una mayor cantidad de paginas web.")


