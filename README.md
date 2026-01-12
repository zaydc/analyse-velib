# Analyse et Visualisation des Données Vélib' 🚲

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ce projet consiste en une analyse approfondie du réseau Vélib' à travers différentes méthodes de visualisation et d'analyse de données. Il comprend des algorithmes de traitement de graphes, des visualisations cartographiques interactives et des analyses statistiques.

## 📋 Fonctionnalités

- **Traitement des données** des stations Vélib'
- **Triangulation de Delaunay** pour analyser la distribution spatiale
- **Diagramme de Voronoï** pour l'analyse de couverture
- **Arbre couvrant minimal** pour optimiser les connexions
- **Cartes interactives** avec Folium
- **Analyse de la répartition** des stations

## 🚀 Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/analyse-velib.git
   cd analyse-velib
   ```

2. Créez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: .\venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Utilisation

### Générer la carte des stations
Pour générer une carte interactive des stations Vélib' :
```bash
python src/main.py generate-map -o results/maps/ma_carte.html
```

### Analyser la répartition des stations
Pour exécuter les analyses de répartition :
```bash
python src/main.py analyze
```

### Générer toutes les visualisations
```bash
# Créer la triangulation de Delaunay
python src/visualization/delaunay.py

# Créer le diagramme de Voronoï
python src/visualization/voronoi_map.py

# Générer l'arbre couvrant minimal
python src/visualization/arbre_couvrant.py
```

### Visualiser les résultats
Ouvrez les fichiers HTML générés dans le dossier `results/maps/` dans votre navigateur préféré.

## 🛠️ Structure du Projet

```
.
├── data/                 # Données brutes et traitées
├── docs/                 # Documentation supplémentaire
├── src/                  # Code source
│   ├── data/             # Scripts de traitement des données
│   ├── utils/            # Utilitaires et fonctions communes
│   └── visualization/    # Scripts de visualisation
├── tests/                # Tests unitaires
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## 📊 Résultats

Les visualisations générées sont disponibles dans les fichiers HTML :
- `stations_map.html` : Carte des stations Vélib'
- `velib_voronoi_map.html` : Diagramme de Voronoï
- `velib_acm_map.html` : Arbre couvrant minimal

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- Données fournies par [Vélib' Métropole](https://www.velib-metropole.fr/)
