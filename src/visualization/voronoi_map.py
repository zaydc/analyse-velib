import json  # Pour manipuler les fichiers JSON
import folium  # Pour créer des cartes interactives
from scipy.spatial import Voronoi  # Pour calculer le diagramme de Voronoi
import numpy as np  # Pour manipuler des tableaux numériques

###################################################################################################
###################################################################################################

# Charger les données des stations
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

# Charger la liste d'adjacence
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
        # Normalisation des valeurs
        Nv_norm = (Nv - 6) / 6
        C_norm = max(C_med - C, 0) / C_med if C_med > 0 else 0
        # Calcul de l'indice (mélange connectivité + capacité restante)
        Ir = alpha * Nv_norm + (1 - alpha) * C_norm
    return Ir


###################################################################################################
###################################################################################################

# Charger les données
stations_data = charger_donnees("station_informations.json")
adjacence_data = charger_liste_adjacence("liste_adjacence.json")

# Vérifier si on a assez de stations pour le diagramme de Voronoi
if len(stations_data) < 3:
    print("Pas assez de stations pour effectuer le diagramme de Voronoi.")
else:
    # Extraction des points valides
    points = np.array([
        [station["lat"], station["lon"]]
        for station in stations_data if "lat" in station and "lon" in station
    ])

    # Vérifier si on a assez de points valides
    if len(points) < 3:
        print("Pas assez de points valides pour le diagramme de Voronoi.")
    else:
        # Calcul du diagramme de Voronoi
        vor = Voronoi(points)

        # Création de la carte centrée sur Paris
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

        # Calcul des indices de répartition
        if adjacence_data:
            # Médiane des capacités pour normaliser C
            capacites = [station.get('capacity') for station in stations_data]
            C_med = np.median(capacites)
            indices = {
                station_id: indice_repartition(
                    len(voisins),
                    next((s.get('capacity', 0) for s in stations_data if str(s["station_id"]) == station_id), 0),
                    C_med
                )
                for station_id, voisins in adjacence_data.items()
            }
        else:
            indices = {}

        # Définition de la fonction pour obtenir une couleur en fonction de l'indice
        def get_color(indice):
            if indice < 0:
                r, g, b = 255, 0, 0  # Rouge pour les indices négatifs
            elif indice == 0:
                r, g, b = 0, 255, 0  # Vert pour un indice nul
            else:
                r, g, b = 0, 0, 255  # Bleu pour les indices positifs
            return f"#{r:02x}{g:02x}{b:02x}"  # Retourner la couleur en format hexadécimal

        # Ajout des cellules de Voronoi à la carte
        for i, region_index in enumerate(vor.point_region):
            if region_index != -1 and len(vor.regions[region_index]) > 0:
                station_id = str(stations_data[i]["station_id"])  # Identifier la station
                indice_rep = indices.get(station_id, 0)  # Récupérer l'indice de répartition
                color = get_color(indice_rep)  # Déterminer la couleur
                polygon = [vor.vertices[j].tolist() for j in vor.regions[region_index]]  # Points du polygone
                folium.Polygon(
                    locations=polygon,  # Ajouter les sommets du polygone
                    color=color,  # Couleur des bords
                    weight=1,  # Épaisseur des bords
                    fill=True,  # Remplir le polygone
                    fill_color=color,  # Couleur de remplissage
                    fill_opacity=0.2  # Opacité du remplissage
                ).add_to(m)

        # Ajout des marqueurs de stations
        for station in stations_data:
            if "lat" in station and "lon" in station:
                station_id = str(station["station_id"])  # Identifier la station
                indice_rep = indices.get(station_id, 0)  # Récupérer l'indice de répartition
                color = get_color(indice_rep)  # Déterminer la couleur
                folium.CircleMarker(
                    location=[station['lat'], station['lon']],  # Position du marqueur
                    radius=5,  # Taille du marqueur
                    color=color,  # Couleur du contour
                    fill=True,  # Remplir le marqueur
                    fill_color=color,  # Couleur de remplissage
                    fill_opacity=0.7,  # Opacité du remplissage
                    tooltip=(  # Info-bulle avec des informations sur la station
                        f"{station.get('name', 'Inconnu')}<br>"
                        f"Capacité: {station.get('capacity', 0)}<br>"
                        f"Indice de répartition: {indice_rep:.3f}"
                    )
                ).add_to(m)

        # Sauvegarde de la carte dans un fichier HTML
        m.save('velib_voronoi_map.html')