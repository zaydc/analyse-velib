import numpy as np  # Pour manipuler des tableaux numériques
import requests  # Pour effectuer des requêtes HTTP
import json  # Pour manipuler les fichiers JSON

# URL du fichier JSON contenant les informations des stations Vélib'
url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"

# Effectuer une requête GET pour télécharger les données
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    data = response.json()  # Convertir la réponse en JSON
    # Sauvegarder les données dans un fichier local
    with open("station_informationn.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)  # Sauvegarder avec une indentation
    print("Le fichier JSON a bien été téléchargé.")  # Confirmation de la sauvegarde
else:
    # Afficher un message d'erreur si la requête a échoué
    print(f"Erreur : {response.status_code}")

###################################################################################################
###################################################################################################

# Nom du fichier contenant les données des stations
FICHIER_ENTREE = "station_informations.json"


# Fonction pour charger et extraire les données des stations Vélib'
def load_station_data():
    """Charge et extrait les données des stations Vélib'."""
    with open(FICHIER_ENTREE, "r", encoding="utf-8") as fichier:
        data = json.load(fichier)  # Charger le contenu du fichier JSON
    
    stations = []  # Liste pour stocker les informations des stations
    coordonnees = []  # Liste pour stocker les coordonnées des stations

    # Vérifier si les données contiennent des stations
    if "data" in data and "stations" in data["data"]:
        for station in data["data"]["stations"]:  # Parcourir chaque station
            stations.append(station)  # Ajouter les informations de la station
            coordonnees.append((station["lat"], station["lon"]))  # Ajouter les coordonnées (latitude, longitude)

    return stations, np.array(coordonnees)  # Retourner les stations et leurs coordonnées sous forme de tableau NumPy

# Code principal
if __name__ == "__main__":
    # Charger les données des stations
    stations, coordonnees = load_station_data()
    # Afficher le nombre de stations chargées
    print(f"Nombre de stations chargées : {len(stations)}")