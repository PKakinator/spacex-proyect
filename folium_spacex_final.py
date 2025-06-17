
# ===============================
# Visualización interactiva de lanzamientos SpaceX con Folium
# ===============================

import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
from math import sin, cos, sqrt, atan2, radians

# ---------- Cargar los datos ----------
df_geo = pd.read_csv("spacex_launch_geo(1).csv")
launch_sites = df_geo.groupby('Launch Site')[['Lat', 'Long']].mean().reset_index()

# ---------- Mapa 1: Sitios de lanzamiento ----------
site_map_1 = folium.Map(location=[28.5, -80.5], zoom_start=4)

for i, row in launch_sites.iterrows():
    folium.Circle(
        [row['Lat'], row['Long']],
        radius=200,  # Radio reducido
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(site_map_1)

    folium.Marker(
        [row['Lat'], row['Long']],
        icon=folium.DivIcon(html=f"<div style='font-size: 12px; color:#000000'><b>{row['Launch Site']}</b></div>")
    ).add_to(site_map_1)

site_map_1.save("mapa1_sitios_lanzamiento.html")

# ---------- Mapa 2: Resultados de lanzamientos (éxito/fallo) ----------
site_map_2 = folium.Map(location=[28.5, -80.5], zoom_start=4)
marker_cluster = MarkerCluster().add_to(site_map_2)

for i, row in df_geo.iterrows():
    color = 'green' if row['class'] == 1 else 'red'
    folium.Marker(
        location=[row['Lat'], row['Long']],
        icon=folium.Icon(color=color),
        popup=f"{row['Launch Site']} - {'Éxito' if row['class'] == 1 else 'Fallo'}"
    ).add_to(marker_cluster)

site_map_2.save("mapa2_resultados.html")

# ---------- Mapa 3: Distancia a punto costero ----------
coast_point = (28.56367, -80.57163)  # coordenada simulada
launch_point = (df_geo.iloc[0]['Lat'], df_geo.iloc[0]['Long'])

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

distance_km = calculate_distance(*launch_point, *coast_point)

site_map_3 = folium.Map(location=launch_point, zoom_start=15)
folium.Marker(launch_point, tooltip="Sitio de lanzamiento").add_to(site_map_3)
folium.Marker(
    coast_point,
    icon=folium.DivIcon(
        icon_size=(20, 20),
        icon_anchor=(0, 0),
        html=f'<div style="font-size: 12px; color:#d35400;"><b>{distance_km:.2f} KM</b></div>'
    )
).add_to(site_map_3)
folium.PolyLine([launch_point, coast_point], color="orange", weight=3).add_to(site_map_3)

site_map_3.save("mapa3_distancia.html")
