import json  # Pour manipuler les fichiers JSON
import folium  # Pour créer des cartes interactives
from folium.plugins import MarkerCluster  # Pour regrouper les marqueurs sur la carte
from scipy.spatial import Delaunay  # Pour effectuer la triangulation de Delaunay
import numpy as np  # Pour manipuler des tableaux numériques
import branca  # Pour ajouter des éléments personnalisés à la carte

###################################################################################################
###################################################################################################

# Charger les données depuis le fichier JSON
with open("station_informations.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Charger le contenu du fichier JSON

# Extraire les stations
stations_data = data.get("data", {}).get("stations", [])  # Récupérer la liste des stations

###################################################################################################
###################################################################################################

# Vérifier si on a assez de points pour la triangulation
if len(stations_data) < 3:
    print("Pas assez de points pour effectuer la triangulation de Delaunay.")
else:
    # Récupérer les coordonnées des stations sous forme de tableau NumPy
    points = np.array([[station["lat"], station["lon"]] for station in stations_data])

    # Appliquer la triangulation de Delaunay
    tri = Delaunay(points)

    # Créer une carte Folium centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=11)

    # Ajouter la triangulation de Delaunay sous forme de polygones
    for simplex in tri.simplices:  # Parcourir chaque triangle de la triangulation
        triangle = [points[i].tolist() for i in simplex]  # Convertir en liste de listes
        folium.Polygon(
            locations=triangle,  # Ajouter les sommets du triangle
            color='black',  # Couleur des lignes
            weight=1,  # Épaisseur des lignes
            fill=True,  # Remplir les triangles
            fill_color='grey',  # Couleur de remplissage
            fill_opacity=0.25  # Opacité du remplissage
        ).add_to(m)

    # Créer un MarkerCluster pour gérer le regroupement des marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    # Ajouter des marqueurs pour chaque station
    for station in stations_data:
        folium.CircleMarker(
            location=[station['lat'], station['lon']],  # Position du marqueur
            radius=max(station.get('capacity', 0) // 5, 3),  # Taille du marqueur (éviter un rayon trop petit)
            color='blue',  # Couleur du contour
            weight=2,  # Épaisseur du contour
            fill=True,  # Remplir le marqueur
            fill_color='blue',  # Couleur de remplissage
            fill_opacity=0.6,  # Opacité du remplissage
            tooltip=f"{station.get('name', 'Inconnu')}<br> Capacité: {station.get('capacity', 0)}"  # Info-bulle avec nom et capacité
        ).add_to(marker_cluster)

    # Créer une légende en HTML
    legend_html = '''
    {% macro html(this, kwargs) %}
    <div style="position: fixed; 
        bottom: 50px; left: 50px; width: 200px; height: 130px; 
        border:2px solid grey; z-index:9999; font-size:14px;
        background-color:white; opacity: 0.85;">
        &nbsp; <b>Légende</b> <br>
        &nbsp; Triangulation de Delaunay &nbsp;<i class="fa fa-circle" style="color:black"></i><br>
        &nbsp; 1 station &nbsp; <i class="fa fa-circle" style="color:blue"></i><br>
        &nbsp; 2 à 9 stations &nbsp; <i class="fa fa-circle" style="color:green"></i><br>
        &nbsp; 10 à 99 stations &nbsp; <i class="fa fa-circle" style="color:yellow"></i><br>
        &nbsp; 100 + stations &nbsp; <i class="fa fa-circle" style="color:orange"></i><br>
    </div>
    {% endmacro %}
    '''

    # Ajouter la légende à la carte
    legende = branca.element.MacroElement()
    legende._template = branca.element.Template(legend_html)
    m.get_root().add_child(legende)

    # Sauvegarder la carte dans un fichier HTML
    m.save('velib_stations_map.html')  # Sauvegarder la carte dans un fichier HTML
    m  # Retourner la carte (utile dans certains environnements)