# functions.py
from urllib.error import HTTPError

from SPARQLWrapper import SPARQLWrapper, JSON
import os
import csv
import tkinter as tk
from tkinter import filedialog
import shutil

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


def getDomainCardinality():
    relation1 = input("Quelle est votre relation dont vous voulez savoir le nombre d'entités? (les relations sont entre P6 et P12615) \n" +
                    "Il peut y avoir des numéros qui ne sont liés à aucune relation \n" +
                    "Attention à mettre le P en majuscule \n")

    rel1 = f"""
    SELECT (COUNT(DISTINCT ?x) AS ?count)
    WHERE {{
    ?x wdt:{relation1} ?y.       
    }}
    """

    def execute_query(query):
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings'][0]['count']['value']

    # Exécuter les requêtes et obtenir les résultats
    dom_R1 = execute_query(rel1)
    print(f"le nombre d'entités pour la relation {relation1} est de : {dom_R1}")

    return dom_R1

# Fin de la fonction 1

def getCoocurence():
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


# fin de la fonction 3

def getFunctionnalDependencies():
    def check_multiple_relations(element, property):
        query = f"""
        SELECT (COUNT(DISTINCT ?y) AS ?count)
        WHERE {{
        wd:{element} wdt:{property} ?y.
        }}
        HAVING (?count > 1)
        """
        
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        # Vérifiez si la requête retourne un résultat avec count > 1
        if results['results']['bindings']:
            return True
        else:
            return False

    while True:
        # Demander à l'utilisateur de saisir l'élément et la propriété
        element = input("Quel est l'élément que vous voulez vérifier ? (par ex., Q76 pour Barack Obama) \n")
        property = input("Quelle est la propriété que vous voulez vérifier ? (par ex., P40 pour parent) \n")
        
        # Vérifier si l'élément a plusieurs relations distinctes pour la propriété
        result = check_multiple_relations(element, property)
        print(f"L'élément {element} avec la propriété {property} a plusieurs relations distinctes: {result}")
        
        # Demander à l'utilisateur s'il veut tester un autre élément
        another = input("Voulez-vous tester un autre élément et une autre propriété ? (oui/non) \n").strip().lower()
        if another != 'oui':
            break

# fin de la fonction 4

def getNumTuples():
    def count_tuples(relation):
        query = f"""
        SELECT (COUNT(*) AS ?count)
        WHERE {{
        ?x wdt:{relation} ?y.
        }}
        """
        
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        
        count = results['results']['bindings'][0]['count']['value']
        return count
    
        
    relation = input("Quelle est la relation que vous voulez vérifier ? (par ex., P40 pour parent) \n")
    count = count_tuples(relation)
    print(f"Le nombre de tuples liés par la relation {relation} est : {count}")

    return count

# fin de la fonction 5

def fun():
    x = int(getDomainCardinality())
    y = int(getNumTuples())
        
    z = x / y
    print(f"Voici le résultat de fonction 1/fonction 5 {z}")
    return z

# fin de la fonction 6

def getSupport():
    def check_implication(relation1, relation2, relation3):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        query = f"""
        SELECT (COUNT(?x) AS ?count)
        WHERE {{
        ?x wdt:{relation1} ?y.
        ?x wdt:{relation2} ?z.
        ?x wdt:{relation3} ?w.
        }}
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        count = results['results']['bindings'][0]['count']['value']
        return count

    # Demander les relations à l'utilisateur
    relation1 = input("Entrez la première relation (par exemple, P26) : ")
    relation2 = input("Entrez la deuxième relation (par exemple, P40) : ")
    relation3 = input("Entrez la troisième relation (par exemple, P25) : ")

    # Exécuter la fonction et afficher le résultat
    result = check_implication(relation1, relation2, relation3)
    print(f"Le nombre de situations où {relation1} et {relation2} impliquent {relation3} est : {result}")

    return result 

# fin de la fonction 7

def getConfidence():
    support = int(getSupport())
    lose = int(getLose())

    if lose != 0:
        confidence = support / lose
        print(f"La confiance est : {confidence}")
    else:
        print("Erreur : Division par zéro. Le dénominateur est zéro.")
# fin de la fonction 9

def getLose():
    def check_implication(relation1, relation2):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        query = f"""
        SELECT (COUNT(?x) AS ?count)
        WHERE {{
        ?x wdt:{relation1} ?y.
        ?x wdt:{relation2} ?z.
        }}
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        count = results['results']['bindings'][0]['count']['value']
        return count

    # Demander les relations à l'utilisateur
    relation1 = input("Entrez la première relation (par exemple, P26) : ")
    relation2 = input("Entrez la deuxième relation (par exemple, P40) : ")

    # Exécuter la fonction et afficher le résultat
    result = check_implication(relation1, relation2)
    print(f"Le nombre de situations où {relation1} et {relation2} est : {result}")

    return result

# fin de la fonction 10


def download_csv():
    csv_file = 'data.csv'
    # Utiliser tkinter pour demander à l'utilisateur où enregistrer le fichier
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        shutil.copyfile(csv_file, file_path)
        print(f"Fichier CSV téléchargé à l'emplacement : {file_path}")