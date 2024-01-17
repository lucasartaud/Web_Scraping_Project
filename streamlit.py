import json
import os
import streamlit as st
import pandas as pd
import plotly.express as px

def text(name, min, max, measure):
    if pd.isna(max):
        return f'{name} : à partir de {min} {measure}'
    elif pd.isna(min):
        return f'{name} : moins de {max} {measure}'
    elif min == max:
        return f'{name} : {min} {measure}'
    else:
        return f'{name} : de {min} à {max} {measure}'

df = pd.read_csv('lunil.csv')

st.markdown(
    """
    <style>
        .block-container {
            max-width: 80vw;
            margin-left: auto;
            margin-right: auto;
        }
        .text-comments {
            font-size: 20px; 
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.write("<h1 style='text-align: center; color:#3E9DF3; font-size: 80px;'>Projet Web Scraping</h1>", unsafe_allow_html=True)
st.write("<h2 style='text-align: center; color:#9A5DFB; font-size: 50px;'>Lucas Artaud & Iswarya Sivasubramaniam DIA 1</h2>", unsafe_allow_html=True)

st.sidebar.header("Pages")
if st.sidebar.selectbox("Sélectionner une page", ["Filtres", "Carte"]) == "Filtres":
    st.sidebar.header("Filtres")

    # Brand:
    enabled_brand = st.sidebar.checkbox("Activer le filtre par marque")
    brand = st.sidebar.selectbox("Filtrer par marque", ['Tesla', 'Renault', 'Mercedes', 'Peugeot', 'NIO'], key='marque') if enabled_brand else 'Tout'
    df_filtered_brand = df[df['Modèle'].str.contains(brand, case=False)] if brand != 'Tout' else df.copy()

    # Price:
    min_possible_price = float(df['Prix (euros) min'].min())
    max_possible_price = float(df['Prix (euros) max'].max())
    min_price, max_price = st.sidebar.slider("Filtrer par prix", min_possible_price, max_possible_price, (min_possible_price, max_possible_price))
    df_filtered_price = df.query(f'not (`Prix (euros) min` > {max_price} or `Prix (euros) max` < {min_price}) and not (`Prix (euros) min`.isnull() and `Prix (euros) max`.isnull())')

    # Acceleration:
    min_possible_acceleration = float(df['Accélération de 0 à 100 km/h (s) min'].min())
    max_possible_acceleration = float(df['Accélération de 0 à 100 km/h (s) max'].max())
    min_acceleration, max_acceleration = st.sidebar.slider("Filtrer par accélération (0 à 100 km/h)", min_possible_acceleration, max_possible_acceleration, (min_possible_acceleration, max_possible_acceleration))
    df_filtered_acceleration = df.query(f'not (`Accélération de 0 à 100 km/h (s) min` > {max_acceleration} or `Accélération de 0 à 100 km/h (s) max` < {min_acceleration}) and not (`Accélération de 0 à 100 km/h (s) min`.isnull() and `Accélération de 0 à 100 km/h (s) max`.isnull())')

    # Battery
    min_possible_battery = float(df['Puissance de la batterie (kWh) min'].min())
    max_possible_battery = float(df['Puissance de la batterie (kWh) max'].max())
    min_battery, max_battery = st.sidebar.slider("Filtrer par la puissance de la batterie (kWh)", min_possible_battery, max_possible_battery, (min_possible_battery, max_possible_battery))
    df_filtered_battery = df.query(f'not (`Puissance de la batterie (kWh) min` > {max_battery} or `Puissance de la batterie (kWh) max` < {min_battery}) and not (`Puissance de la batterie (kWh) min`.isnull() and `Puissance de la batterie (kWh) max`.isnull())')

    # Speed
    min_possible_speed = float(df['Vitesse maximale (km/h) min'].min())
    max_possible_speed = float(df['Vitesse maximale (km/h) max'].max())
    min_speed, max_speed = st.sidebar.slider("Filtrer par vitesse maximale (km/h)", min_possible_speed, max_possible_speed, (min_possible_speed, max_possible_speed))
    df_filtered_speed = df.query(f'not (`Vitesse maximale (km/h) min` > {max_speed} or `Vitesse maximale (km/h) max` < {min_speed}) and not (`Vitesse maximale (km/h) min`.isnull() and `Vitesse maximale (km/h) max`.isnull())')

    # Autonomy
    min_possible_autonomy = float(df['Autonomie (km) min'].min())
    max_possible_autonomy = float(df['Autonomie (km) max'].max())
    min_autonomy, max_autonomy = st.sidebar.slider("Filtrer par autonomie (km)", min_possible_autonomy, max_possible_autonomy, (min_possible_autonomy, max_possible_autonomy))
    df_filtered_autonomy = df.query(f'not (`Autonomie (km) min` > {max_autonomy} or `Autonomie (km) max` < {min_autonomy}) and not (`Autonomie (km) min`.isnull() and `Autonomie (km) max`.isnull())')

    # Weight
    min_possible_weight = float(df['Poids (kg) min'].min())
    max_possible_weight = float(df['Poids (kg) max'].max())
    min_weight, max_weight = st.sidebar.slider("Filtrer par poids (kg)", min_possible_weight, max_possible_weight, (min_possible_weight, max_possible_weight))
    df_filtered_weight = df.query(f'not (`Poids (kg) min` > {max_weight} or `Poids (kg) max` < {min_weight}) and not (`Poids (kg) min`.isnull() and `Poids (kg) max`.isnull())')

    # Surface
    df['Surface (m2)'] = df['Longueur (mm)'] * df['Largeur (mm)'] / 1000000
    min_possible_surface = float(df['Surface (m2)'].min())
    max_possible_surface = float(df['Surface (m2)'].max())
    min_surface, max_surface = st.sidebar.slider("Filtrer par surface (m²)", min_possible_surface, max_possible_surface, (min_possible_surface, max_possible_surface))
    df_filtered_surface = df.query(f'{min_surface} <= `Surface (m2)` and `Surface (m2)` <= {max_surface} and not `Surface (m2)`.isnull()')

    # st.write("df_filtered_brand")
    # st.dataframe(df_filtered_brand)
    # st.write("df_filtered_price")
    # st.dataframe(df_filtered_price)
    # st.write("df_filtered_acceleration")
    # st.dataframe(df_filtered_acceleration)
    # st.write("df_filtered_battery")
    # st.dataframe(df_filtered_battery)
    # st.write("df_filtered_speed")
    # st.dataframe(df_filtered_speed)
    # st.write("df_filtered_autonomy")
    # st.dataframe(df_filtered_autonomy)
    # st.write("df_filtered_weight")
    # st.dataframe(df_filtered_weight)
    # st.write("df_filtered_surface")
    # st.dataframe(df_filtered_surface)

    df_filtered_final = pd.merge(pd.merge(pd.merge(pd.merge(pd.merge(pd.merge(pd.merge(df_filtered_brand, df_filtered_price, how='inner'), df_filtered_acceleration, how='inner'), df_filtered_battery, how='inner'), df_filtered_speed, how='inner'), df_filtered_autonomy, how='inner'), df_filtered_weight, how='inner'), df_filtered_surface, how='inner')
    st.header('Résultats du filtrage', divider='blue')    
    # st.dataframe(df_filtered_final)
    col1, col2, col3, col4 = st.columns(4)
    for index, row in df_filtered_final.iterrows():
        with col1 if index % 4 == 0 else col2 if index % 4 == 1 else col3 if index % 4 == 2 else col4:
            st.image(f'images/{row["Modèle"]}.jpg', use_column_width=True)
            st.write(f"<p style='text-align: center;'>{row['Modèle']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='text-align: center;'>{text('Prix', row['Prix (euros) min'], row['Prix (euros) max'], 'euros')}</p>", unsafe_allow_html=True)
            st.write(f"<p style='text-align: center;'>{text('Accélération de 0 à 100 km/h', row['Accélération de 0 à 100 km/h (s) min'], row['Accélération de 0 à 100 km/h (s) min'], 'secondes')}</p>", unsafe_allow_html=True)
            st.write(f"<p style='text-align: center;'>{text('Puissance de la batterie', row['Puissance de la batterie (kWh) min'], row['Puissance de la batterie (kWh) max'], 'kWh')}</p>", unsafe_allow_html=True)
            st.write(f"<p style='text-align: center;'>{text('Vitesse maximale', row['Vitesse maximale (km/h) min'], row['Vitesse maximale (km/h) max'], 'km/h')}</p>", unsafe_allow_html=True)
            st.write(f"<p style='text-align: center;'>{text('Autonomie', row['Autonomie (km) min'], row['Autonomie (km) max'], 'km')}</p>", unsafe_allow_html=True)
            st.write(f"<p style='text-align: center;'>{text('Poids', row['Poids (kg) min'], row['Poids (kg) max'], 'kg')}</p>", unsafe_allow_html=True)
            st.write(f"<p style='text-align: center;'>{'Surface : ' + str(row['Surface (m2)']) + ' m²'}</p>", unsafe_allow_html=True)

else:
    with open("consolidation-etalab-schema-irve-statique-v-2.2.0-20240116.json", "r") as file:
        data = json.load(file)

    # Création d'un DataFrame avec les données des stations
    stations = []
    for feature in data['features']:
        coordinates = feature['geometry']['coordinates']
        name = feature['properties']['nom_station']
        stations.append({'Name': name, 'Latitude': coordinates[1], 'Longitude': coordinates[0]})

    df_stations = pd.DataFrame(stations)

    # Création d'une carte avec plotly express
    fig = px.scatter_mapbox(df_stations, 
                            lat='Latitude', 
                            lon='Longitude', 
                            text='Name', 
                            hover_name='Name',
                            zoom=5)

    # Configuration du style et de la taille de la carte
    fig.update_layout(mapbox_style='open-street-map', width=1600, height=800)

    # Affichage de la carte dans Streamlit
    st.header('Carte des stations de recharge électrique', divider='blue')
    st.plotly_chart(fig)
