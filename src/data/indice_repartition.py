# Importation des bibliothèques nécessaires
import json  # Pour manipuler les fichiers JSON
import folium  # Pour créer des cartes interactives
from folium.plugins import MarkerCluster  # Pour regrouper les marqueurs sur la carte
from scipy.spatial import Delaunay  # Pour effectuer la triangulation de Delaunay
import numpy as np  # Pour manipuler des tableaux numériques

###################################################################################################
###################################################################################################

# Charger les données des stations depuis un fichier JSON
def charger_donnees(fichier_json):
    try:
        with open(fichier_json, "r", encoding="utf-8") as file:
            data = json.load(file)  # Charger le contenu du fichier JSON
        return data.get("data", {}).get("stations", [])  # Retourner la liste des stations
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")  # Gérer les erreurs
        return []
    
###################################################################################################
###################################################################################################

# Charger la liste d'adjacence depuis un fichier JSON
def charger_liste_adjacence(fichier):
    try:
        with open(fichier, 'r', encoding="utf-8") as f:
            return json.load(f)  # Charger le contenu du fichier JSON
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors du chargement de la liste d'adjacence : {e}")  # Gérer les erreurs
        return {}

###################################################################################################
###################################################################################################

# Fonction pour calculer l'indice de répartition
def indice_repartition(Nv, C, C_med, alpha=0.5):
    # Si le nombre de voisins est égal à 6, l'indice est 0
    if Nv == 6:
        Ir = 0
    else:
        # Normalisation du nombre de voisins
        Nv_norm = (Nv - 6) / 6
        # Normalisation de la capacité restante
        C_norm = max(C_med - C, 0) / C_med if C_med > 0 else 0
        # Calcul de l'indice en combinant les deux critères
        Ir = alpha * Nv_norm + (1 - alpha) * C_norm
    return Ir  # Retourner l'indice

###################################################################################################
###################################################################################################

# Charger les données des stations
stations_data = charger_donnees("station_informations.json")
# Charger la liste d'adjacence
adjacence_data = charger_liste_adjacence("liste_adjacence.json")

# Vérifier qu'il y a suffisamment de stations pour la triangulation
if len(stations_data) < 3:
    print("Pas assez de stations pour effectuer la triangulation de Delaunay.")
else:
    # Extraire les coordonnées des stations valides
    points = np.array([
        [station["lat"], station["lon"]]
        for station in stations_data if "lat" in station and "lon" in station
    ])

    # Vérifier qu'il y a suffisamment de points valides
    if len(points) < 3:
        print("Pas assez de points valides pour la triangulation.")
    else:
        # Effectuer la triangulation de Delaunay
        tri = Delaunay(points)

        # Créer une carte centrée sur Paris
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

        # Ajouter les triangles de Delaunay à la carte
        for simplex in tri.simplices:
            triangle = [points[i].tolist() for i in simplex]  # Convertir les points en liste
            folium.Polygon(
                locations=triangle,  # Ajouter les sommets du triangle
                color='black',  # Couleur des bords
                weight=1,  # Épaisseur des bords
                fill=True,  # Remplir le triangle
                fill_color='grey',  # Couleur de remplissage
                fill_opacity=0.25  # Opacité du remplissage
            ).add_to(m)

        # Calculer les indices de répartition pour chaque station
        indices = {}
        # Calculer la médiane des capacités des stations
        capacites = [station.get('capacity', 0) for station in stations_data]
        C_med = np.median(capacites) if capacites else 0  # Éviter une erreur si la liste est vide

        for station in stations_data:
            station_id = str(station["station_id"])  # Identifier la station
            Nv = len(adjacence_data.get(station_id, [])) if adjacence_data else 0  # Nombre de voisins
            C = station.get('capacity', 0)  # Capacité de la station
            indices[station_id] = indice_repartition(Nv, C, C_med)  # Calculer l'indice

        # Fonction pour déterminer la couleur en fonction de l'indice
        def get_color(indice_rep):
            indice_rep = max(-1, min(indice_rep, 1))  # Normaliser entre -1 et 1

            if indice_rep < 0:
                r = 255  # Rouge au maximum
                g = int(50 * (1 + indice_rep))  # Vert faible pour les indices négatifs
            else:
                r = int(255 * (0.8 - indice_rep))  # Rouge diminue pour les indices positifs
                g = 255  # Vert au maximum pour les indices positifs

            return f"#{r:02x}{g:02x}00"  # Retourner la couleur en format hexadécimal

        # Ajouter les marqueurs des stations sur la carte
        for station in stations_data:
            if "lat" in station and "lon" in station:
                station_id = str(station["station_id"])  # Identifier la station
                indice_rep = indices.get(station_id, 0)  # Récupérer l'indice de répartition

                color = get_color(indice_rep)  # Déterminer la couleur du marqueur

                folium.CircleMarker(
                    location=[station['lat'], station['lon']],  # Position du marqueur
                    radius=max(station.get('capacity', 0) // 6, 4),  # Taille du marqueur
                    color=color,  # Couleur du contour
                    weight=5,  # Épaisseur du contour
                    fill=True,  # Remplir le marqueur
                    fill_color=color,  # Couleur de remplissage
                    fill_opacity=0.9,  # Opacité du remplissage
                    tooltip=(  # Ajouter une info-bulle
                        f"{station.get('name', 'Inconnu')}<br>"
                        f"Capacité: {station.get('capacity', 0)}<br>"
                        f"Indice de répartition: {indice_rep:.3f}"
                    )
                ).add_to(m)

        # Sauvegarder la carte dans un fichier HTML
        m.save('velib_stations_map.html')