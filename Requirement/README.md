# Projet SAE 202 - Analyse et Visualisation des Stations Vélib'

Ce projet a pour objectif d'analyser et de visualiser les données des stations Vélib' à Paris à l'aide de divers outils et algorithmes. Voici une description détaillée des fonctionnalités de chaque fichier inclus dans ce projet.

---

## **Fichiers et Fonctionnalités**

### 1. **`process_data.py`**
- **Description** : Ce fichier est responsable de la récupération et du traitement des données des stations Vélib'.
- **Fonctionnalités** :
  - Télécharge les données des stations depuis une API et les sauvegarde dans un fichier JSON local.
  - Charge les données des stations et extrait leurs coordonnées (latitude, longitude).
- **Exécution** : Peut être exécuté directement pour vérifier le nombre de stations chargées.

---

### 2. **`voronoi.py`**
- **Description** : Génère un diagramme de Voronoi basé sur les coordonnées des stations.
- **Fonctionnalités** :
  - Charge les données des stations depuis un fichier JSON.
  - Calcule et affiche le diagramme de Voronoi à l'aide de `matplotlib`.

---

### 3. **`voronoi_map.py`**
- **Description** : Crée une carte interactive avec les cellules de Voronoi pour chaque station.
- **Fonctionnalités** :
  - Charge les données des stations et une liste d'adjacence.
  - Calcule un indice de répartition pour chaque station en fonction de sa connectivité et de sa capacité.
  - Génère une carte interactive avec les cellules de Voronoi colorées selon l'indice de répartition.
  - Sauvegarde la carte dans un fichier HTML (`velib_voronoi_map.html`).

---

### 4. **`view_map_stations.py`**
- **Description** : Affiche une carte interactive des stations Vélib' avec des marqueurs.
- **Fonctionnalités** :
  - Charge les données des stations.
  - Affiche chaque station sur une carte Folium avec un marqueur dont la taille dépend de la capacité de la station.
  - Sauvegarde la carte dans un fichier HTML (`stations_map.html`).

---

### 5. **`map_triangulation.py`**
- **Description** : Génère une carte interactive avec la triangulation de Delaunay des stations.
- **Fonctionnalités** :
  - Calcule la triangulation de Delaunay à partir des coordonnées des stations.
  - Affiche les triangles sur une carte interactive.
  - Ajoute des marqueurs pour chaque station.
  - Sauvegarde la carte dans un fichier HTML (`velib_stations_map.html`).

---

### 6. **`liste_adjacence.py`**
- **Description** : Génère une liste d'adjacence des stations basée sur la triangulation de Delaunay.
- **Fonctionnalités** :
  - Calcule la triangulation de Delaunay.
  - Crée une liste d'adjacence où chaque station est connectée à ses voisins dans la triangulation.
  - Sauvegarde (sous forme de dictiononnaire) la liste d'adjacence dans un fichier JSON (`liste_adjacence.json`).

---

### 7. **`indice_repartition.py`**
- **Description** : Calcule et visualise un indice de répartition pour chaque station.
- **Fonctionnalités** :
  - Charge les données des stations et la liste d'adjacence.
  - Calcule un indice de répartition basé sur la connectivité et la capacité des stations.
  - Génère une carte interactive avec des marqueurs colorés selon l'indice de répartition.
  - Sauvegarde la carte dans un fichier HTML (`velib_stations_map.html`).

---

### 8. **`delaunay.py`**
- **Description** : Visualise la triangulation de Delaunay des stations à l'aide de `matplotlib`.
- **Fonctionnalités** :
  - Charge les coordonnées des stations.
  - Calcule et affiche la triangulation de Delaunay sous forme de graphique.

---

### 9. **`arbre_couvrant.py`**
- **Description** : Calcule et visualise l'arbre couvrant minimum (ACM) des stations.
- **Fonctionnalités** :
  - Charge une liste d'adjacence et les coordonnées des stations.
  - Construit un graphe des stations et calcule l'ACM à l'aide de l'algorithme de Kruskal.
  - Affiche l'ACM sur une carte interactive avec Folium.
  - Sauvegarde la carte dans un fichier HTML (`velib_acm_map.html`).

---

## **Comment Utiliser le Projet**
1. Assurez-vous d'avoir Python installé sur votre machine.
2. Installez les dépendances nécessaires avec la commande :
   ```bash
   pip install -r requirements.txt