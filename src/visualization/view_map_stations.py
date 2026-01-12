import folium  # Pour créer des cartes interactives
from process_data import load_station_data  # Importer la fonction pour charger les données des stations
from folium.plugins import MarkerCluster  # Pour regrouper les marqueurs sur la carte

###################################################################################################
###################################################################################################

# Charger les données des stations
stations, _ = load_station_data()

# Création de la carte centrée sur Paris
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Ajouter un marqueur pour chaque station
for station in stations:
    folium.CircleMarker(
        location=[station['lat'], station['lon']],  # Position du marqueur (latitude, longitude)
        popup=station["name"],  # Info-bulle affichant le nom de la station
        radius=station['capacity'] // 4,  # Taille du marqueur proportionnelle à la capacité
        color='blue',  # Couleur du contour
        weight=1,  # Épaisseur du contour
        fill=True,  # Remplir le marqueur
        fill_color='blue'  # Couleur de remplissage
    ).add_to(m)

# Sauvegarde de la carte dans un fichier HTML
m.save("stations_map.html")

# Affichage de la carte (utile dans un environnement Jupyter Notebook)
m