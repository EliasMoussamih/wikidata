# Projet d'Analyse de Données SPARQL

## Description du Projet

Ce projet permet d'extraire et d'analyser des données provenant de Wikidata en utilisant des requêtes SPARQL. Il inclut des fonctionnalités pour importer des données CSV dans une base de données SQLite, exécuter des requêtes SPARQL pour obtenir diverses statistiques et analyser des relations entre différentes entités.

## Fonctionnalités Principales

1. **Importation CSV vers SQLite** : Importer des données à partir d'un fichier CSV et créer une table SQLite pour stocker ces données.
2. **Analyse de Cardinalité** : Obtenir le nombre d'entités distinctes pour une relation donnée.
3. **Cooccurrence de Relations** : Déterminer combien d'entités ont deux relations spécifiques et enregistrer le résultat dans un fichier CSV.
4. **Vérification de Dépendances Fonctionnelles** : Vérifier si un élément possède plusieurs relations distinctes pour une propriété donnée.
5. **Calcul du Nombre de Tuples** : Obtenir le nombre de tuples pour une relation spécifique.
6. **Calcul du Ratio d'Entités Distinctes par Nombre de Tuples**.
7. **Support des Relations** : Calculer le nombre de situations où deux relations impliquent une troisième relation.
8. **Couverture de Tête** : Calculer le taux de couverture de tête pour des relations spécifiques.
9. **Confiance des Relations** : Calculer le pourcentage de confiance entre deux relations avec implication.
10. **Téléchargement de CSV** : Télécharger le fichier CSV contenant les données analysées.

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/projet-sparql.git
