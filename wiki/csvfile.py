import os
import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import tkinter as tk
from tkinter import filedialog
import shutil

# Définir l'endpoint SPARQL (par exemple, Wikidata)
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Lire la liste des relations à partir du fichier CSV
relations_file = 'path/to/Wikidata_Database_reports_List_of_properties_all_1.csv'  # Remplacez par le chemin correct
relations = []

with open(relations_file, mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        relations.append(row[0])  # Assuming the relation (property) is in the first column

def append_to_csv(file_path, data):
    file_exists = os.path.isfile(file_path)
    if file_exists:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if (row[0] == data[0] and row[1] == data[1]) or (row[0] == data[1] and row[1] == data[0]):
                    return  # Doublon trouvé, on ne fait rien

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['R1', 'R2', 'dom_intersection', 'dom_R1', 'dom_R2'])
        writer.writerow(data)

def execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings'][0]['count']['value']

# Ajouter les résultats au fichier CSV
csv_file = 'data.csv'
if not os.path.isfile(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['R1', 'R2', 'dom_intersection', 'dom_R1', 'dom_R2'])

# Boucles imbriquées pour tester toutes les combinaisons de relations
for i in range(len(relations)):
    for j in range(i + 1, len(relations)):
        relation1 = relations[i]
        relation2 = relations[j]

        # Définir les requêtes SPARQL
        liaison = f"""
        SELECT (COUNT(distinct ?x) AS ?count)
        WHERE {{
          ?x wdt:{relation1} ?y.       
          ?x wdt:{relation2} ?z.
        }}
        """

        rel1 = f"""
        SELECT (COUNT(DISTINCT ?x) AS ?count)
        WHERE {{
          ?x wdt:{relation1} ?y.       
        }}
        """

        rel2 = f"""
        SELECT (COUNT(DISTINCT ?x) AS ?count)
        WHERE {{
          ?x wdt:{relation2} ?y.       
        }}
        """

        try:
            # Exécuter les requêtes et obtenir les résultats
            dom_R1 = execute_query(rel1)
            print(f"le nombre d'entités pour la relation {relation1} est de : {dom_R1}")

            dom_R2 = execute_query(rel2)
            print(f"le nombre d'entités pour la relation {relation2} est de : {dom_R2}")

            dom_intersection = execute_query(liaison)
            print(f"le nombre d'entités pour les deux relations est de : {dom_intersection}")

            # Ajouter les résultats au fichier CSV
            append_to_csv(csv_file, [relation1, relation2, dom_intersection, dom_R1, dom_R2])

        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête pour {relation1} et {relation2}: {e}")

# Demander à l'utilisateur s'il veut télécharger le fichier CSV
download = input("Voulez-vous télécharger le fichier CSV ? (oui/non) \n").strip().lower()

if download == "oui":
    # Utiliser tkinter pour demander à l'utilisateur où enregistrer le fichier
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        shutil.copyfile(csv_file, file_path)
        print(f"Fichier CSV téléchargé à l'emplacement : {file_path}")
