import json  # Pour manipuler les fichiers JSON
import numpy as np  # Pour manipuler des tableaux numériques
from scipy.spatial import Delaunay  # Pour effectuer la triangulation de Delaunay
import sys  # Pour configurer l'encodage de sortie

###################################################################################################
###################################################################################################

# Forcer l'encodage UTF-8 pour éviter les erreurs d'encodage
sys.stdout.reconfigure(encoding='utf-8')

# Charger le fichier JSON original contenant les informations des stations
with open("station_informations.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Charger le contenu du fichier JSON

# Extraire les données nécessaires
stations = data["data"]["stations"]  # Liste des stations
coordonnees = [(s["lon"], s["lat"]) for s in stations]  # Extraire les coordonnées (longitude, latitude)
station_ids = [s["station_id"] for s in stations]  # Extraire les IDs des stations

# Triangulation de Delaunay
points = np.array(coordonnees)  # Convertir les coordonnées en tableau NumPy
tri = Delaunay(points)  # Effectuer la triangulation de Delaunay

# Création de la liste d'adjacence
adj_list = {station_id: set() for station_id in station_ids}  # Initialiser un dictionnaire avec des ensembles vides

###################################################################################################
###################################################################################################

# Ajouter les connexions entre les stations
for simplex in tri.simplices:  # Parcourir chaque triangle de la triangulation
    s1, s2, s3 = simplex  # Indices des stations dans la liste
    id1, id2, id3 = station_ids[s1], station_ids[s2], station_ids[s3]  # Récupérer les IDs des stations

    # Ajouter les connexions entre les stations du triangle
    adj_list[id1].update([id2, id3])
    adj_list[id2].update([id1, id3])
    adj_list[id3].update([id1, id2])

# Convertir les ensembles en listes pour l'affichage et la sauvegarde
adj_list = {station: list(neighbors) for station, neighbors in adj_list.items()}

# Afficher la liste d'adjacence
for station, neighbors in adj_list.items():
    print(f"Station {station} → {neighbors}")  # Afficher chaque station et ses voisins

# Sauvegarder la liste d'adjacence dans un fichier JSON
with open("liste_adjacence.json", "w", encoding="utf-8") as f:
    json.dump(adj_list, f, indent=4)  # Sauvegarder le dictionnaire dans un fichier JSON avec une indentation

# Indiquer que la sauvegarde a été effectuée
print("Liste d'adjacence sauvegardée dans 'liste_adjacence.json'.")