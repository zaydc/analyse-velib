"""
Point d'entrée principal pour l'analyse des données Vélib'.
Ce script permet d'exécuter les différentes analyses et visualisations du projet.
"""
import argparse
import sys
from pathlib import Path

# Ajout du répertoire parent au chemin Python pour les imports
sys.path.append(str(Path(__file__).parent.parent))

def main():
    parser = argparse.ArgumentParser(description="Analyse des données Vélib'")
    
    # Sous-commandes
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande pour générer la carte des stations
    map_parser = subparsers.add_parser('generate-map', help='Générer la carte des stations')
    map_parser.add_argument('--output', '-o', type=str, default='results/maps/stations_map.html',
                          help='Fichier de sortie pour la carte')
    
    # Commande pour analyser la répartition
    analyze_parser = subparsers.add_parser('analyze', help='Analyser la répartition des stations')
    analyze_parser.add_argument('--output-dir', '-o', type=str, default='results/analysis',
                              help='Dossier de sortie pour les analyses')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'generate-map':
        from visualization.view_map_stations import generate_map
        generate_map(args.output)
        print(f"Carte générée avec succès : {args.output}")
    
    elif args.command == 'analyze':
        from data.indice_repartition import analyze_distribution
        from data.liste_adjacence import generate_adjacency_list
        
        print("Analyse de la répartition des stations...")
        analyze_distribution()
        
        print("\nGénération de la liste d'adjacence...")
        generate_adjacency_list()
        
        print("\nAnalyse terminée. Les résultats sont disponibles dans le dossier 'results/analysis'")

if __name__ == "__main__":
    main()
