import os
import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import tkinter as tk
from tkinter import filedialog
import shutil

# Définir l'endpoint SPARQL (par exemple, Wikidata)
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Demander les relations
relation1 = input("Quelle est votre première relation ? (les relations sont entre P6 et P12615) \n" +
                  "Il peut y avoir des numéros qui ne sont liés à aucune relation \n" +
                  "Attention à mettre le P en majuscule \n")

relation2 = input("Quelle est votre deuxième relation ? \n")

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

# Exécuter les requêtes et obtenir les résultats
dom_R1 = execute_query(rel1)
print(f"le nombre d'entités pour la relation {relation1} est de : {dom_R1}")

dom_R2 = execute_query(rel2)
print(f"le nombre d'entités pour la relation {relation2} est de : {dom_R2}")

dom_intersection = execute_query(liaison)
print(f"le nombre d'entités pour les deux relations est de : {dom_intersection}")

# Ajouter les résultats au fichier CSV
csv_file = 'data.csv'
append_to_csv(csv_file, [relation1, relation2, dom_intersection, dom_R1, dom_R2])

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
