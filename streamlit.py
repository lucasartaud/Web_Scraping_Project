import streamlit as st
import pandas as pd

# Charger le DataFrame depuis le fichier CSV
df = pd.read_csv('lunil.csv')

# Titre de l'application
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

# Sidebar pour les filtres
st.sidebar.header("Filtres")

# Filtrer par marque
marque_enabled = st.sidebar.checkbox("Activer le filtre par marque")
marque = st.sidebar.selectbox("Filtrer par marque", ['Tesla', 'Renault', 'Mercedes'], key='marque') if marque_enabled else 'Tout'
df_filtre_marque = df[df['Modèle'].str.contains(marque, case=False)] if marque != 'Tout' else df.copy()

# Filtrer par prix
prix_enabled = st.sidebar.checkbox("Activer le filtre par prix")
prix = st.sidebar.slider("Filtrer par prix", float(df['Prix (euros) min'].min()), float(df['Prix (euros) max'].max()))  if prix_enabled else None
df_filtre_prix = df[(df['Prix (euros) min'].isnull() | (df['Prix (euros) min'] <= prix)) & (df['Prix (euros) max'].isnull() | (df['Prix (euros) max'] >= prix))] if prix_enabled else df.copy()

# Filtrer par accélération
acceleration_enabled = st.sidebar.checkbox("Activer le filtre par accélération")
acceleration = st.sidebar.slider("Filtrer par accélération (0 à 100 km/h)", float(df['Accélération de 0 à 100 km/h (s) min'].min()), float(df['Accélération de 0 à 100 km/h (s) max'].max())) if acceleration_enabled else None
df_filtre_acceleration = df[(df['Accélération de 0 à 100 km/h (s) min'].isnull() | (df['Accélération de 0 à 100 km/h (s) min'] <= acceleration)) & (df['Accélération de 0 à 100 km/h (s) max'].isnull() | (df['Accélération de 0 à 100 km/h (s) max'] >= acceleration))] if acceleration_enabled else df.copy()

# Filtrer par vitesse maximale
vitesse_enabled = st.sidebar.checkbox("Activer le filtre par vitesse maximale")
vitesse = st.sidebar.slider("Filtrer par vitesse maximale (km/h)", float(df['Vitesse maximale (km/h) min'].min()), float(df['Vitesse maximale (km/h) max'].max())) if vitesse_enabled else None
df_filtre_vitesse = df[(df['Vitesse maximale (km/h) min'].isnull() | (df['Vitesse maximale (km/h) min'] <= vitesse)) & (df['Vitesse maximale (km/h) max'].isnull() | (df['Vitesse maximale (km/h) max'] >= vitesse))] if vitesse_enabled else df.copy()

# st.write("df_filtre_marque")
# st.dataframe(df_filtre_marque)
# st.write("df_filtre_prix")
# st.dataframe(df_filtre_prix)
# st.write("df_filtre_acceleration")
# st.dataframe(df_filtre_acceleration)
# st.write("df_filtre_vitesse")
# st.dataframe(df_filtre_vitesse)

# Afficher le DataFrame filtré
df_filtre_final = pd.merge(pd.merge(pd.merge(df_filtre_marque, df_filtre_prix, how='inner'), df_filtre_acceleration, how='inner'), df_filtre_vitesse, how='inner')
# st.write("df_filtre_final")
st.dataframe(df_filtre_final)
