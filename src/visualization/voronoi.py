import numpy as np  # Pour manipuler des tableaux numériques
import matplotlib.pyplot as plt  # Pour visualiser les données
import json  # Pour manipuler les fichiers JSON
from scipy.spatial import Voronoi, voronoi_plot_2d  # Pour calculer et visualiser le diagramme de Voronoi

###################################################################################################
###################################################################################################

# Charger les données depuis le fichier JSON
with open("station_informations.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Charger le contenu du fichier JSON

# Extraire les données des stations
stations_data = data.get("data", {}).get("stations", [])  # Récupérer la liste des stations

# Extraire les coordonnées des stations sous forme de tableau NumPy
points = np.array([[station["lat"], station["lon"]] for station in stations_data])

# Calculer le diagramme de Voronoi à partir des coordonnées
vor = Voronoi(points)

# Visualiser le diagramme de Voronoi
fig = voronoi_plot_2d(vor)  # Générer la figure du diagramme

###################################################################################################
###################################################################################################

plt.show()  # Afficher la figure