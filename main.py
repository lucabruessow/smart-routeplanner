import streamlit as st
import ollama
import folium
from streamlit_folium import st_folium

st.session_state.setdefault('route_points', [])

st.title("KI Routenplaner")


st.subheader("Karte")

# Karte erstellen
karte = folium.Map(
    location = [50.96282, 14.07066],
    zoom_start = 18
)

# Normalen und Satellitenlayer hinzufügen
folium.TileLayer('OpenStreetMap').add_to(karte)
folium.TileLayer(
    tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr = 'Esri',
    name = 'Satellit',
    overlay = False,
    control = True
    ).add_to(karte)

folium.LayerControl().add_to(karte)

# Karte anzeigen
map_data = st_folium(karte, width=700, height=500)

# Klickevent verarbeiten
if map_data['last_clicked']:
    st.write('Koordinaten: ', map_data['last_clicked']['lat'], map_data['last_clicked']['lng'])
    st.session_state.route_points.append([map_data['last_clicked']['lat'], map_data['last_clicked']['lng']])