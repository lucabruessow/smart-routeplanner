import streamlit as st
import ollama
import folium
import requests
from streamlit_folium import st_folium
import polyline

st.session_state.setdefault('route_points', [])
st.session_state.setdefault('zoom', 18)
st.session_state.setdefault('location', [50.96282, 14.07066])

def get_route_from_osrm(waypoints):
    if len(waypoints) < 2:
        return None
    
    coords = ";".join([f'{point[1]},{point[0]}' for point in waypoints])

    url = f'http://router.project-osrm.org/route/v1/driving/{coords}'
    params = {
        'overview': 'full',
        'geometries': 'polyline',
        'steps': 'true'
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['routes']:
                return data['routes'][0]
        return None
    except Exception as e:
        st.error(f'Fehler beim Abrufen der Route: {e}')
        return None
    
    
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

if len(st.session_state.route_points) >= 2:
    route_data = get_route_from_osrm(st.session_state.route_points)

    if route_data:
        route_coords = polyline.decode(route_data['geometry'])

        folium.PolyLine(
            locations = route_coords,
            color = 'blue',
            weight = 5,
            popup = f'Entfernung: {route_data['distance'] / 1000: .2f} km\nDauer: {route_data['duration'] / 60: .0f} min'
        ).add_to(m)
    st.info(f'Entfernung: {route_data['distance'] / 1000: .2f} km\nDauer: {route_data['duration'] / 60: .0f} min')

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