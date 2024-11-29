import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Cargar el dataset
pf = pd.read_csv("spotify_songs_dataset.csv")
image_path = "pages/Necesarios/fondo_morado.png"

# Codificar la imagen en base64
with open(image_path, "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode()

# Aplicar estilo de fondo a la aplicación
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #f0f0f0;
    }}
    
    .stButton > button {{
        background-color: #6a0dad;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #9b4de1;
    }}
    
    .stHeader {{
        color: #ffffff;
    }}
    
    .stTitle {{
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
    }}
    
    .stText {{
        font-size: 16px;
        color: #d1d1d1;
    }}
    
    .stMarkdown {{
        color: #d1d1d1;
    }}
    
    table {{
        width: 100%;
        margin-top: 20px;
        border-collapse: collapse;
    }}
    
    table, th, td {{
        border: 1px solid #d1d1d1;
        text-align: left;
    }}
    
    th {{
        background-color: #9b4de1;
        color: white;
        padding: 10px;
    }}
    
    td {{
        background-color: #3c2a5e;
        color: white;
        padding: 8px;
    }}
    
    .stSelectbox, .stSlider {{
        background-color: #9b4de1;
        color: white;
        border-radius: 5px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Configuración inicial para la página y subpágina actual
if "page" not in st.session_state:
    st.session_state.page = "inicio"

if "subpage" not in st.session_state:
    st.session_state.subpage = None

# Función para cambiar la página principal
def cambiar_pagina(nueva_pagina):
    st.session_state.page = nueva_pagina
    if nueva_pagina != "categoría_2":
        st.session_state.subpage = None  # Resetear la subpágina solo si no estamos en "categoría_2"

def cambiar_subpagina(nueva_subpagina):
    st.session_state.subpage = nueva_subpagina

st.title("Spotify Dataset")

if st.session_state.page == "inicio":
    st.header("Seleccione una opción")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Dataset"):
            cambiar_pagina("categoría_1")
    with col2:
        if st.button("Gaficos"):
            cambiar_pagina("categoría_2")
    
    with col3:
        if st.button("Analisis"):
            cambiar_pagina("categoría_3")

#Organizacion de la segunda pagina y categorias
#Categoria 1 Dataset
elif st.session_state.page == "categoría_1":
    opciones = ["Todo"] + pf.columns.tolist()  
    seleccion = st.selectbox("Selecciona una columna para ver", opciones)

    if seleccion == "Todo":
        st.write("Base de datos completa:")
        st.dataframe(pf) 
    else:
        st.write(f"Columna seleccionada: {seleccion}")
        st.write(pf[seleccion])
    if st.button("Volver atrás"):
        cambiar_pagina("inicio")
#Categoria 2 Graficos
elif st.session_state.page == "categoría_2":
    if st.session_state.subpage is None:
        st.header("Seleccione una subcategoría")
        if st.button("Gráfico de Contenido Explícito"):
            cambiar_subpagina("subcategoria_a")
        if st.button("Distribución de Idioma de Canciones"):
            cambiar_subpagina("subcategoria_b")
        if st.button("Tendencia de Lanzamiento de Canciones"):
            cambiar_subpagina("subcategoria_c")
        if st.button("Duración Promedio por Género"):
            cambiar_subpagina("subcategoria_d")
        if st.button("Duración vs Reproducciónes"):
            cambiar_subpagina("subcategoria_e")
        
        if st.button("Volver atrás"):
            cambiar_pagina("inicio")
    
    else:
        if st.session_state.subpage == "subcategoria_a":
            st.header("Subcategoría A: Contenido Explícito")
            st.write("Aquí se mostrarán los datos de la Subcategoría A.")
            pf_filtrado_2 = pf.dropna(subset=['genre', 'explicit_content'])
            contenido_filtrado = pf
            opcion_contenido = st.selectbox('Selecciona el tipo de contenido:', 
                                ['Todos', 'Contenido Explícito', 'Sin Contenido Explícito'])
            if opcion_contenido == 'Contenido Explícito':
                data_filtrada = pf[pf['explicit_content'] == 'Yes']
            elif opcion_contenido == 'Sin Contenido Explícito':
                data_filtrada = pf[pf['explicit_content'] == 'No']
            else:
                data_filtrada = pf
            contenido_explicito = data_filtrada.groupby(['genre', 'explicit_content']).size().unstack(fill_value=0)

            fig, ax = plt.subplots(figsize=(12, 8))
            contenido_explicito.plot(kind='bar', stacked=True, ax=ax)
            ax.set_title('Proporción de Canciones con Contenido Explícito por Género')
            ax.set_xlabel('Género')
            ax.set_ylabel('Número de Canciones')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            plt.tight_layout()

            st.pyplot(fig)
            if st.button("Volver atrás"):
                cambiar_pagina("inicio")
            
        elif st.session_state.subpage == "subcategoria_b":
            if 'language' not in pf.columns:
                st.error("La columna 'language' no se encuentra en el dataset.")
            else:
                st.title("Distribución de Idiomas por Género")

                selected_genres = st.multiselect(
                    "Selecciona los géneros que deseas analizar:",
                    options=pf['genre'].dropna().unique()
                )

                filtered_data = pf[pf['genre'].isin(selected_genres)] if selected_genres else pf

                if filtered_data.empty:
                    st.warning("No hay datos para los géneros seleccionados.")
                else:
                    language_counts = filtered_data['language'].dropna().value_counts().reset_index()
                    language_counts.columns = ['language', 'count']

                    fig = px.pie(                      
                        language_counts,
                        names='language',
                        values='count',
                        title='Distribución de Idiomas',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )

                    st.plotly_chart(fig)
                    if st.button("Volver atrás"):
                        cambiar_pagina("inicio")
                    
        elif st.session_state.subpage == "subcategoria_c":
            st.header("Tendencia de Lanzamiento de Canciones")
            st.write("Aquí se mostrarán los datos de la Subcategoría C.")
            pf['release_date'] = pd.to_datetime(pf['release_date'], errors='coerce')
            pf_filtrado = pf.dropna(subset=['release_date'])
            pf_filtrado['year'] = pf_filtrado['release_date'].dt.year

            generos = pf_filtrado['genre'].dropna().unique()
            genero_seleccionado = st.selectbox('Selecciona un género musical:', options=generos)
            pf_filtrado_genero = pf_filtrado[pf_filtrado['genre'] == genero_seleccionado]

            min_year = int(pf_filtrado_genero['year'].min())
            max_year = int(pf_filtrado_genero['year'].max())
            rango_años = st.slider('Selecciona el rango de años:', min_year, max_year, (min_year, max_year))

            pf_filtrado_rango = pf_filtrado_genero[(pf_filtrado_genero['year'] >= rango_años[0]) & (pf_filtrado_genero['year'] <= rango_años[1])]

            releases_by_year = pf_filtrado_rango.groupby('year').size()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(releases_by_year.index, releases_by_year.values, marker='o')
            ax.set_title(f"Tendencia de Lanzamientos de Canciones en {genero_seleccionado} ({rango_años[0]}-{rango_años[1]})")
            ax.set_xlabel("Año")
            ax.set_ylabel("Número de Canciones")
            ax.grid(True)
            st.pyplot(fig)
            if st.button("Volver atrás"):
                cambiar_pagina("inicio")
                
        elif st.session_state.subpage == "subcategoria_d":
            st.header("Duración Promedio de Canciones por Género") 
            genero_filtrado = pf[['genre', 'duration']]
            genero_filtrado = genero_filtrado.dropna(subset=['genre', 'duration'])
            
            st.title("Duración de Canciones por Género")
            genero_unico = genero_filtrado['genre'].unique()
            seleccionar_genero = st.selectbox("Selecciona un género de música:", options=['Todos'] + list(genero_unico))
            fig, ax = plt.subplots(figsize=(10, 6))
            if seleccionar_genero == 'Todos':
                duracion_por_genero = genero_filtrado.groupby('genre')['duration'].mean().sort_values()
                
                duracion_por_genero.plot(kind='barh', ax=ax, color='skyblue')
                ax.set_title('Duración Promedio de Canciones por Género')
                ax.set_xlabel('Duración Promedio (segundos)')
                ax.set_ylabel('Género')
            else:
                canciones_genero = genero_filtrado[genero_filtrado['genre'] == seleccionar_genero]
                
                ax.barh(canciones_genero.index, canciones_genero['duration'], color='red')
                ax.set_title(f'Duración de Canciones en Género: {seleccionar_genero}')
                ax.set_xlabel('Duración (segundos)')
                ax.set_ylabel('Canción')
            plt.tight_layout()
            st.pyplot(fig)
            if st.button("Volver atrás"):
                cambiar_pagina("inicio")
                
        elif st.session_state.subpage == "subcategoria_e":
            st.header("Duración vs Reproducciones")
            st.markdown("Este gráfico muestra cómo la duración de las canciones se relaciona con las reproducciones, categorizado por género.")

            if pf.empty or 'duration' not in pf.columns or 'stream' not in pf.columns:
                st.error("El dataset no contiene las columnas necesarias para generar el gráfico.")
            else:
                genres = pf['genre'].dropna().unique()
                selected_genres = st.multiselect("Selecciona uno o varios géneros:", options=genres)

                if not selected_genres:
                    st.warning("Selecciona al menos un género para mostrar el gráfico.")
                else:
                    filtered_data = pf[pf['genre'].isin(selected_genres)]

                    if filtered_data.empty:
                        st.warning("No hay datos disponibles para los géneros seleccionados.")
                    else:
                        fig = px.scatter(
                            filtered_data,
                            x='duration',
                            y='stream',
                            color='genre',
                            size='popularity',
                            title="Duración vs Reproducciones",
                            labels={"duration": "Duración (segundos)", "stream": "Reproducciones", "genre": "Género"},
                            template="plotly_white",
                            opacity=0.7
                        )

                        st.plotly_chart(fig)
            
                        if st.button("Volver atrás"):
                            cambiar_pagina("inicio")
                
            if st.button("Volver atrás"):
                st.session_state.subpage = None

elif st.session_state.page == "categoría_3":
    st.header("Análisis de Datos")
    st.write("A continuación, se presenta el análisis de la base de datos, organizado según los gráficos generados:")
    
    st.subheader("1. Contenido Explícito")
    st.write("""
         De este gráfico se pueden inferir dos conclusiones principales:
         1. La diferencia entre canciones con y sin contenido explícito no varía mucho, pero las canciones con contenido explícito son ligeramente más abundantes.
         2. Los géneros con más canciones son la electrónica, el hip-hop y el pop.
    """)
    
    st.subheader("2. Distribución de Idiomas por Género")
    st.write("""
        Este gráfico sugiere que los lenguajes más abundantes en los géneros no suelen variar mucho, con diferencias de pequeñas décimas. 
        Los idiomas, de mayor a menor frecuencia, son: inglés, español, francés, coreano, italiano, japonés y alemán. 
        Los últimos tres tienden a variar entre los últimos puestos.
    """)
    
    st.subheader("3. Tendencia de Lanzamiento de Canciones")
    st.write("""
        De este gráfico se pueden deducir dos puntos clave:
        1. Las canciones comienzan a registrarse desde 1995, probablemente porque a partir de ese año se documentaron digitalmente.
        2. Cada género presenta un pico definido en algún momento de la línea de tiempo, alcanzando su máximo en un solo período específico.
    """)
    
    st.subheader("4. Duración de Canciones por Género")
    st.write("""
        Este gráfico muestra que la duración promedio de las canciones es consistente entre géneros, alrededor de 240 segundos.
    """)
        
    st.subheader("5. Duración vs Reproducciones")
    st.write("""
        Se observa que, aunque las canciones de cualquier duración pueden ser muy escuchadas, la mayoría de las canciones más reproducidas tienen una duración entre 200 y 300 segundos.
    """)

    
    if st.button("Volver atrás"):
        cambiar_pagina("inicio")
