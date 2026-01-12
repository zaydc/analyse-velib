# Importation des bibliothèques nécessaires
import json  # Pour manipuler les fichiers JSON
import networkx as nx  # Pour créer et manipuler des graphes
import matplotlib.pyplot as plt  # Pour visualiser les graphes
import folium  # Pour créer des cartes interactives
import branca  # Pour ajouter une légende aux cartes

# Étape 1 : Chargement des Données
def charger_donnees(fichier_json):
    # Ouvre et charge le contenu d'un fichier JSON
    with open(fichier_json, "r") as file:
        return json.load(file)

# Étape 2 : Construction du graphe à partir de la liste d'adjacence
def construire_graphe(liste_adjacence):
    # Crée un graphe non orienté
    G = nx.Graph()
    # Ajoute les arêtes au graphe à partir de la liste d'adjacence
    for station, voisins in liste_adjacence.items():
        for voisin in voisins:
            G.add_edge(int(station), int(voisin))  # Ajoute une arête entre deux stations
    return G

# Étape 3 : Calcul de l'Arbre Couvrant Minimum (ACM) avec Kruskal
def calculer_acm(graphe):
    # Calcule l'ACM en utilisant l'algorithme de Kruskal
    return nx.minimum_spanning_tree(graphe, algorithm="kruskal")

# Étape 4 : Visualisation de l'ACM
def afficher_acm(acm):
    # Configure la taille de la figure pour l'affichage
    plt.figure(figsize=(12, 8))
    # Calcule la disposition des nœuds pour le graphe
    pos = nx.spring_layout(acm)
    # Dessine le graphe avec les nœuds et les arêtes
    nx.draw(acm, pos, with_labels=False, node_size=50, edge_color="blue")
    # Ajoute un titre au graphique
    plt.title("Arbre Couvrant Minimum des Stations")
    # Affiche le graphique
    plt.show()

# Chargement des coordonnées des stations depuis un fichier JSON
def charger_coordonnees(fichier_json):
    # Ouvre et charge le fichier JSON
    with open(fichier_json, 'r') as file:
        data = json.load(file)
    # Extrait les coordonnées des stations
    stations = data.get("data", {}).get("stations", [])
    # Retourne un dictionnaire avec les coordonnées (latitude, longitude) des stations
    return {str(station["station_id"]): (station["lat"], station["lon"]) for station in stations}

# Affichage de l'ACM sur une carte interactive avec folium
def afficher_acm_folium(acm, coordonnees_stations):
    # Crée une carte centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Ajoute les stations sur la carte
    for station, (lat, lon) in coordonnees_stations.items():
        folium.CircleMarker(location=[lat, lon], radius=3, color="red", fill=True, fill_color="red").add_to(m)

    # Ajoute les connexions de l'ACM sur la carte
    for u, v in acm.edges():
        # Vérifie que les stations existent dans les coordonnées
        if str(u) in coordonnees_stations and str(v) in coordonnees_stations:
            lat1, lon1 = coordonnees_stations[str(u)]
            lat2, lon2 = coordonnees_stations[str(v)]
            # Trace une ligne entre les deux stations
            folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue", weight=1.5).add_to(m)
        else:
            # Affiche un message si une station est manquante
            print(f"Pas de correspondance pour l'arête ({u}, {v}) dans les coordonnées des stations.")

    # Ajoute une légende à la carte
    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 250px;
        height: 120px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        ">
        <b>Légende :</b><br>
        <i style="color:red;">●</i> Stations Vélib'<br>
        <i style="color:blue;">━</i> Connexions ACM<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m

# Programme principal
if __name__ == "__main__":
    # Nom du fichier contenant la liste d'adjacence
    fichier_json = "liste_adjacence.json"
    # Charge la liste d'adjacence
    liste_adjacence = charger_donnees(fichier_json)
    # Construit le graphe à partir de la liste d'adjacence
    G = construire_graphe(liste_adjacence)
   
    # Affiche le nombre de nœuds et d'arêtes dans le graphe
    print(f"Nombre de stations (nœuds) : {G.number_of_nodes()}")
    print(f"Nombre de connexions (arêtes) : {G.number_of_edges()}")
 
    # Calcule l'ACM du graphe
    ACM = calculer_acm(G)
    # Affiche le nombre d'arêtes dans l'ACM
    print(f"Nombre de connexions dans l'ACM : {ACM.number_of_edges()}")
   
    # Affiche l'ACM sous forme de graphe
    afficher_acm(ACM)
    # Nom du fichier contenant les informations des stations
    fichier_stations = "station_informations.json"
    # Charge les coordonnées des stations
    coordonnees_stations = charger_coordonnees(fichier_stations)
    
    # Affiche l'ACM sur une carte interactive
    carte = afficher_acm_folium(ACM, coordonnees_stations)
    
    # Sauvegarde la carte dans un fichier HTML
    carte.save("velib_acm_map.html")
    # Retourne la carte (utile pour l'affichage dans certains environnements)
    carte