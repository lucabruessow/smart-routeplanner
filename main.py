import streamlit as st
import ollama
import folium
from streamlit_folium import st_folium

st.session_state.setdefault('route_points', [])
st.session_state.setdefault('zoom', 18)
st.session_state.setdefault('location', [50.96282, 14.07066])

st.title("KI Routenplaner")
st.subheader("Karte")

# Karte erstellen
m = folium.Map(
    location = st.session_state.location,
    zoom_start = st.session_state.zoom
)

# Normalen und Satellitenlayer hinzufügen
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer(
    tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr = 'Esri',
    name = 'Satellit',
    show = False,
    overlay = True,
    control = True
    ).add_to(m)

folium.LayerControl().add_to(m)

for i, coord in enumerate(st.session_state.route_points):
    folium.Marker(
        location=coord,
        popup=f"{i+1}. Wegpunkt",
        tooltip=f"{i+1}. Wegpunkt"
    ).add_to(m)

# Karte rendern
map = st_folium(m, width=700, height=500)

# Klickevent verarbeiten
if map['last_clicked']:
    lat, lng = map['last_clicked']['lat'], map['last_clicked']['lng']
    st.write('Koordinaten: ', lat, lng)

    # Neuen Punkt
    st.session_state.route_points.append([lat, lng])
    st.session_state.location = [map['center']['lat'], map['center']['lng']]
    st.session_state.zoom = map['zoom']
    st.rerun()