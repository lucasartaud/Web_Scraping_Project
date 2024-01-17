import streamlit as st
import pandas as pd

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

# Speed
min_possible_speed = float(df['Vitesse maximale (km/h) min'].min())
max_possible_speed = float(df['Vitesse maximale (km/h) max'].max())
min_speed, max_speed = st.sidebar.slider("Filtrer par vitesse maximale (km/h)", min_possible_speed, max_possible_speed, (min_possible_speed, max_possible_speed))
df_filtered_speed = df.query(f'not (`Vitesse maximale (km/h) min` > {max_speed} or `Vitesse maximale (km/h) max` < {min_speed}) and not (`Vitesse maximale (km/h) min`.isnull() and `Vitesse maximale (km/h) max`.isnull())')

# st.write("df_filtered_brand")
# st.dataframe(df_filtered_brand)
# st.write("df_filtered_price")
# st.dataframe(df_filtered_price)
# st.write("df_filtered_acceleration")
# st.dataframe(df_filtered_acceleration)
# st.write("df_filtered_speed")
# st.dataframe(df_filtered_speed)

df_filtered_final = pd.merge(pd.merge(pd.merge(df_filtered_brand, df_filtered_price, how='inner'), df_filtered_acceleration, how='inner'), df_filtered_speed, how='inner')

# st.write("df_filtered_final")
st.dataframe(df_filtered_final)
