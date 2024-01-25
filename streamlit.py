import json
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
        h1 {
            font-size: 80px;
            text-align: center;
            color:#3E9DF3;
        }
        h2 {
            font-size: 50px;
            text-align: center;
            color:#9A5DFB;
        }
        h3 {
            font-size: 40px;
        }
        h4 {
            font-size: 30px;
            text-align: center;
        }
        p {
            font-size: 15px;
            text-align: center;
        }
        .bold {
            font-weight: bold;
            color:#B22222;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.write(f"<h3>Pages</h3>", unsafe_allow_html=True)
selected_page = st.sidebar.selectbox("Sélectionner une page", ["Accueil", "Filtres", "Économies", "Carte"])

if selected_page == "Accueil":
    st.write("<h1>Projet Web Scraping</h1>", unsafe_allow_html=True)
    st.write("<h2>Lucas Artaud & Iswarya Sivasubramaniam DIA 1</h2>", unsafe_allow_html=True)
    st.image("images/image_d'accueil.jpg", use_column_width=True)
    st.write("<h3>Les transports représentent 24% des émissions totales de CO2 dans le monde, et même 43% en France !</h3>", unsafe_allow_html=True)
    st.write("<h3>Le but de notre projet est de répertorier les voitures électriques des différentes marques avec leur caractéristiques et donner la possibilité à l'utilisateur de naviguer et découvrir les différents modèles. À partir de ces données, nous allons conseiller aux utilisateurs la voiture adaptée à leurs besoins.</h3>", unsafe_allow_html=True)
    st.write("<h3>L'utilisateur peut renseigner ses critères, comme le prix, l'accélération, la puissance de la batterie, la vitesse maximale, l'autonomie, le poids, la longueur et la largeur. Il peut également visualiser les économies de carburant réalisées par voiture. Enfin, l'utilisateur peut voir les bornes de recharges près de chez lui.</h3>", unsafe_allow_html=True)
    st.write("<h3>Veuillez sélectionner une page en haut à gauche.</h3>", unsafe_allow_html=True)

elif selected_page == "Filtres":
    st.sidebar.write(f"<h3>Filtres</h3>", unsafe_allow_html=True)

    # Brand:
    enabled_brand = st.sidebar.checkbox("Activer le filtre par marque")
    brand = st.sidebar.selectbox("Filtrer par marque", ['Tesla', 'Renault', 'Mercedes', 'Peugeot', 'NIO'], key='marque') if enabled_brand else 'Tout'
    df_filtered = df[df['Modèle'].str.contains(brand, case=False)] if brand != 'Tout' else df.copy()

    # Price:
    min_possible_price = float(df['Prix (euros) min'].min())
    max_possible_price = float(df['Prix (euros) max'].max())
    min_price, max_price = st.sidebar.slider("Filtrer par prix", min_possible_price, max_possible_price, (min_possible_price, max_possible_price))
    df_filtered = df_filtered.query(f'not (`Prix (euros) min` > {max_price} or `Prix (euros) max` < {min_price}) and not (`Prix (euros) min`.isnull() and `Prix (euros) max`.isnull())')

    # Acceleration:
    min_possible_acceleration = float(df['Accélération de 0 à 100 km/h (s) min'].min())
    max_possible_acceleration = float(df['Accélération de 0 à 100 km/h (s) max'].max())
    min_acceleration, max_acceleration = st.sidebar.slider("Filtrer par accélération (0 à 100 km/h)", min_possible_acceleration, max_possible_acceleration, (min_possible_acceleration, max_possible_acceleration))
    df_filtered = df_filtered.query(f'not (`Accélération de 0 à 100 km/h (s) min` > {max_acceleration} or `Accélération de 0 à 100 km/h (s) max` < {min_acceleration}) and not (`Accélération de 0 à 100 km/h (s) min`.isnull() and `Accélération de 0 à 100 km/h (s) max`.isnull())')

    # Battery:
    min_possible_battery = float(df['Puissance de la batterie (kWh) min'].min())
    max_possible_battery = float(df['Puissance de la batterie (kWh) max'].max())
    min_battery, max_battery = st.sidebar.slider("Filtrer par la puissance de la batterie (kWh)", min_possible_battery, max_possible_battery, (min_possible_battery, max_possible_battery))
    df_filtered = df_filtered.query(f'not (`Puissance de la batterie (kWh) min` > {max_battery} or `Puissance de la batterie (kWh) max` < {min_battery}) and not (`Puissance de la batterie (kWh) min`.isnull() and `Puissance de la batterie (kWh) max`.isnull())')

    # Speed:
    min_possible_speed = float(df['Vitesse maximale (km/h) min'].min())
    max_possible_speed = float(df['Vitesse maximale (km/h) max'].max())
    min_speed, max_speed = st.sidebar.slider("Filtrer par vitesse maximale (km/h)", min_possible_speed, max_possible_speed, (min_possible_speed, max_possible_speed))
    df_filtered = df_filtered.query(f'not (`Vitesse maximale (km/h) min` > {max_speed} or `Vitesse maximale (km/h) max` < {min_speed}) and not (`Vitesse maximale (km/h) min`.isnull() and `Vitesse maximale (km/h) max`.isnull())')

    # Autonomy:
    min_possible_autonomy = float(df['Autonomie (km) min'].min())
    max_possible_autonomy = float(df['Autonomie (km) max'].max())
    min_autonomy, max_autonomy = st.sidebar.slider("Filtrer par autonomie (km)", min_possible_autonomy, max_possible_autonomy, (min_possible_autonomy, max_possible_autonomy))
    df_filtered = df_filtered.query(f'not (`Autonomie (km) min` > {max_autonomy} or `Autonomie (km) max` < {min_autonomy}) and not (`Autonomie (km) min`.isnull() and `Autonomie (km) max`.isnull())')

    # Weight:
    min_possible_weight = float(df['Poids (kg) min'].min())
    max_possible_weight = float(df['Poids (kg) max'].max())
    min_weight, max_weight = st.sidebar.slider("Filtrer par poids (kg)", min_possible_weight, max_possible_weight, (min_possible_weight, max_possible_weight))
    df_filtered = df_filtered.query(f'not (`Poids (kg) min` > {max_weight} or `Poids (kg) max` < {min_weight}) and not (`Poids (kg) min`.isnull() and `Poids (kg) max`.isnull())')

    # Length:
    min_possible_length = float(df['Longueur (mm)'].min())
    max_possible_length = float(df['Longueur (mm)'].max())
    min_length, max_length = st.sidebar.slider("Filtrer par longueur (mm)", min_possible_length, max_possible_length, (min_possible_length, max_possible_length))
    df_filtered = df_filtered.query(f'{min_length} <= `Longueur (mm)` and `Longueur (mm)` <= {max_length} and not `Longueur (mm)`.isnull()')

    # Width:
    min_possible_width = float(df['Largeur (mm)'].min())
    max_possible_width = float(df['Largeur (mm)'].max())
    min_width, max_width = st.sidebar.slider("Filtrer par largeur (mm)", min_possible_width, max_possible_width, (min_possible_width, max_possible_width))
    df_filtered = df_filtered.query(f'{min_width} <= `Largeur (mm)` and `Largeur (mm)` <= {max_width} and not `Largeur (mm)`.isnull()')

    st.write(f"<h2>Résultats du filtrage</h2>", unsafe_allow_html=True)
    df_filtered.reset_index(inplace=True)
    col1, col2, col3, col4 = st.columns(4)
    for index, row in df_filtered.iterrows():
        with col1 if index % 4 == 0 else col2 if index % 4 == 1 else col3 if index % 4 == 2 else col4:
            st.image(f'images/{row["Modèle"]}.jpg', use_column_width=True)
            st.write(f"<h4>{row['Modèle']}</h4>", unsafe_allow_html=True)
            st.write(f"<p>{text('Prix', row['Prix (euros) min'], row['Prix (euros) max'], 'euros')}</p>", unsafe_allow_html=True)
            st.write(f"<p>{text('Accélération de 0 à 100 km/h', row['Accélération de 0 à 100 km/h (s) min'], row['Accélération de 0 à 100 km/h (s) min'], 'secondes')}</p>", unsafe_allow_html=True)
            st.write(f"<p>{text('Puissance de la batterie', row['Puissance de la batterie (kWh) min'], row['Puissance de la batterie (kWh) max'], 'kWh')}</p>", unsafe_allow_html=True)
            st.write(f"<p>{text('Vitesse maximale', row['Vitesse maximale (km/h) min'], row['Vitesse maximale (km/h) max'], 'km/h')}</p>", unsafe_allow_html=True)
            st.write(f"<p>{text('Autonomie', row['Autonomie (km) min'], row['Autonomie (km) max'], 'km')}</p>", unsafe_allow_html=True)
            st.write(f"<p>{text('Poids', row['Poids (kg) min'], row['Poids (kg) max'], 'kg')}</p>", unsafe_allow_html=True)
            st.write(f"<p>{'Longueur : ' + str(row['Longueur (mm)']) + ' mm'}</p>", unsafe_allow_html=True)
            st.write(f"<p>{'Largeur : ' + str(row['Largeur (mm)']) + ' mm'}</p>", unsafe_allow_html=True)

elif selected_page == "Économies":
    df_pdf = pd.read_csv('comparatif_VE.csv')
    df_merged = pd.merge(df, df_pdf, how='inner', left_on='Modèle', right_on='Marque / Modèle')

    st.write(f"<h2>Économies réalisées grâce à l'électrique</h2>", unsafe_allow_html=True)
    actual_consumption = st.sidebar.text_input("Quelle est la consommation de carburant de votre voiture thermique en litres par 100 km ?")
    price_per_litre = st.sidebar.text_input("Quel est le prix du litre de carburant en euros ?")
    number_of_kilometers = st.sidebar.text_input("Combien de kilomètres parcourez-vous par an ?")
    autonomy_required = st.sidebar.text_input("De combien de kilomètres d'autonomie quotidiennement avez-vous besoin ?")
    price_required = st.sidebar.text_input("Quel est votre budget pour l'achat d'une voiture électrique ?")

    try:
        if actual_consumption != '':
            actual_consumption = actual_consumption.replace(',', '.')
            actual_consumption = float(actual_consumption)

        if price_per_litre != '':
            price_per_litre = price_per_litre.replace(',', '.')
            price_per_litre = float(price_per_litre)

        if number_of_kilometers != '':
            number_of_kilometers = float(number_of_kilometers)

        if autonomy_required != '':
            autonomy_required = float(autonomy_required)
            df_merged = df_merged.query(f'`Autonomie (km) min` >= {autonomy_required} or `Autonomie (km) max` >= {autonomy_required}')

        if price_required != '':
            price_required = float(price_required)
            df_merged = df_merged.query(f'`Prix (euros) min` <= {price_required} or `Prix (euros) max` <= {price_required}')
    
        df_merged['Économies'] = ((number_of_kilometers / 100) * actual_consumption * price_per_litre - (number_of_kilometers / 100) * df_merged['Coût au 100km (WLTP)']).astype(int)

        df_merged.reset_index(inplace=True)
        col1, col2, col3, col4 = st.columns(4)
        for index, row in df_merged.iterrows():
            with col1 if index % 4 == 0 else col2 if index % 4 == 1 else col3 if index % 4 == 2 else col4:
                st.image(f'images/{row["Modèle"]}.jpg', use_column_width=True)
                st.write(f"<h4>{row['Modèle']}</h4>", unsafe_allow_html=True)
                st.write(f"<p>{text('Prix', row['Prix (euros) min'], row['Prix (euros) max'], 'euros')}</p>", unsafe_allow_html=True)
                st.write(f"<p>{text('Accélération de 0 à 100 km/h', row['Accélération de 0 à 100 km/h (s) min'], row['Accélération de 0 à 100 km/h (s) min'], 'secondes')}</p>", unsafe_allow_html=True)
                st.write(f"<p>{text('Puissance de la batterie', row['Puissance de la batterie (kWh) min'], row['Puissance de la batterie (kWh) max'], 'kWh')}</p>", unsafe_allow_html=True)
                st.write(f"<p>{text('Vitesse maximale', row['Vitesse maximale (km/h) min'], row['Vitesse maximale (km/h) max'], 'km/h')}</p>", unsafe_allow_html=True)
                st.write(f"<p>{text('Autonomie', row['Autonomie (km) min'], row['Autonomie (km) max'], 'km')}</p>", unsafe_allow_html=True)
                st.write(f"<p>{text('Poids', row['Poids (kg) min'], row['Poids (kg) max'], 'kg')}</p>", unsafe_allow_html=True)
                st.write(f"<p>{'Longueur : ' + str(row['Longueur (mm)']) + ' mm'}</p>", unsafe_allow_html=True)
                st.write(f"<p>{'Largeur : ' + str(row['Largeur (mm)']) + ' mm'}</p>", unsafe_allow_html=True)
                st.write(f"<p class='bold'>{'Économies annuelles : ' + str(row['Économies']) + ' euros'}</p>", unsafe_allow_html=True)

    except:
        st.write(f"<h3>Veuillez entrer des valeurs numériques.</h3>", unsafe_allow_html=True)

elif selected_page == "Carte":
    with open("consolidation-etalab-schema-irve-statique-v-2.2.0-20240116.json", "r") as file:
        data = json.load(file)

    # Creation of a DataFrame with station data
    stations = []
    for feature in data['features']:
        coordinates = feature['geometry']['coordinates']
        name = feature['properties']['nom_station']
        stations.append({'Name': name, 'Latitude': coordinates[1], 'Longitude': coordinates[0]})

    df_stations = pd.DataFrame(stations)

    # Creation of a map with Plotly Express
    fig = px.scatter_mapbox(df_stations, 
                            lat='Latitude', 
                            lon='Longitude', 
                            text='Name', 
                            hover_name='Name',
                            zoom=5)

    # Configuration of the map
    fig.update_layout(mapbox_style='open-street-map', height=800)

    # Display of the map
    st.write(f"<h2>Carte des stations de recharge électrique</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
