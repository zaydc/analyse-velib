# Importation des bibliothèques nécessaires
import numpy as np  # Pour manipuler des tableaux de données numériques
from scipy.spatial import Delaunay  # Pour effectuer la triangulation de Delaunay
import matplotlib.pyplot as plt  # Pour visualiser les données

###################################################################################################
###################################################################################################

# Importation d'une fonction personnalisée pour charger les données des stations
from process_data import load_station_data

# Charger les données des stations Vélib' à partir d'une source externe
stations, _ = load_station_data()

# Extraction des coordonnées (latitude, longitude) des stations
coords = np.array([[station['lat'], station['lon']] for station in stations])

# Création de la triangulation de Delaunay à partir des coordonnées
delaunay = Delaunay(coords)

###################################################################################################
###################################################################################################


# Visualisation de la triangulation
plt.figure(figsize=(8, 6))  # Définir la taille de la figure
plt.triplot(coords[:, 1], coords[:, 0], delaunay.simplices, color='r')  # Dessiner les triangles
plt.scatter(coords[:, 1], coords[:, 0], marker='o', color='b')  # Dessiner les points des stations
plt.xlabel("Longitude")  # Étiquette pour l'axe des X
plt.ylabel("Latitude")  # Étiquette pour l'axe des Y
plt.title("Triangulation de Delaunay des stations Vélib'")  # Titre du graphique
plt.show()  # Afficher le graphique