from urllib.error import HTTPError
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import csv
import tkinter as tk
from tkinter import filedialog
import shutil
import re
from typing import List, Tuple


# Définir la classe Atom pour représenter chaque atome
class Atom:
    def __init__(self, relation: str, argumentLeft: str, argumentRight: str):
        self.relation = relation
        self.argumentLeft = argumentLeft
        self.argumentRight = argumentRight

    def __repr__(self):
        return f"Atom(relation='{self.relation}', argumentLeft='{self.argumentLeft}', argumentRight='{self.argumentRight}')"

def parse_horn_clause(rule: str) -> Tuple[List[Atom], Atom]:
    body_part, head_part = rule.split(" => ")
   
    # Expression régulière pour extraire la relation et les arguments
    atom_pattern = re.compile(r"(\w+)\((\w+)\s*,\s*(\w+)\)")
   
    # Parser la tête
    head_match = atom_pattern.match(head_part)
    if head_match:
        head_atom = Atom(*head_match.groups())
    else:
        raise ValueError("Format de tête invalide")

    # Parser le corps
    body_atoms = []
    for atom_str in body_part.split(", "):
        body_match = atom_pattern.match(atom_str)
        if body_match:
            body_atoms.append(Atom(*body_match.groups()))
        else:
            raise ValueError("Format d'atome du corps invalide")
   
    return body_atoms, head_atom

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


def getDomainCardinality(relation1):
    """
    Obtient le nombre d'entités distinctes pour une relation donnée.

    Args:
        relation1 (str): La relation à vérifier (par exemple, "P26").

    Returns:
        int: Le nombre d'entités distinctes pour la relation donnée.
    """
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

# fin de la fonction 1



def getCoocurence(relation1, relation2):
    """
    Savoir combien d'entités ont deux relations particulières enregistre le résultat dans un fichier CSV.

    Args:
        relation1 (str): La première relation à vérifier.
        relation2 (str): La deuxième relation à vérifier.
    """
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
        """
        Ajoute des données à un fichier CSV, en évitant les doublons.

        Args:
            file_path (str): Le chemin du fichier CSV.
            data (list): Les données à ajouter.
        """
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



def getFunctionnalDependencies(element, property):
    """
    Vérifie si un élément a plusieurs relations distinctes pour une propriété donnée.

    Args:
        element (str): L'élément à vérifier (par exemple, "Q76" pour Barack Obama).
        property (str): La propriété à vérifier (par exemple, "P40" pour parent).
    """
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
        # Vérifier si l'élément a plusieurs relations distinctes pour la propriété
        result = check_multiple_relations(element, property)
        print(f"L'élément {element} avec la propriété {property} a plusieurs relations distinctes: {result}")
        
        # Demander à l'utilisateur s'il veut tester un autre élément
        another = input("Voulez-vous tester un autre élément et une autre propriété ? (oui/non) \n").strip().lower()
        if another != 'oui':
            break

# fin de la fonction 4



def getNumTuples(relation):
    """
    Obtient le nombre de tuples pour une relation donnée.

    Args:
        relation (str): La relation à vérifier (par exemple, "P40" pour parent).

    Returns:
        int: Le nombre de tuples liés par la relation donnée.
    """
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

    count = count_tuples(relation)
    print(f"Le nombre de tuples liés par la relation {relation} est : {count}")

    return count

# fin de la fonction 5



def fun(relation):
    """
    Calcule le rapport entre le nombre d'entités distinctes et le nombre de tuples pour une relation donnée.

    Args:
        relation (str): La relation à vérifier.

    Returns:
        float: Le rapport entre le nombre d'entités distinctes et le nombre de tuples.
    """
    DomainCardinality = int(getDomainCardinality(relation))
    NumTuples = int(getNumTuples(relation))
        
    fun = DomainCardinality / NumTuples
    print(f"Voici le résultat de fonction 1/fonction 5 {fun}")
    return fun

# fin de la fonction 6



def getSupport(relation1, relation2, relation3):
    """
    Obtient le nombre de situations où deux relations impliquent une troisième relation.

    Args:
        relation1 (str): La première relation.
        relation2 (str): La deuxième relation.
        relation3 (str): La troisième relation.

    Returns:
        int: Le nombre de situations où les deux premières relations impliquent la troisième.
    """
    def check_implication(relation1, relation2, relation3):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        query = f"""
        SELECT (COUNT(?x) AS ?count)
        WHERE {{
        ?x wdt:{relation1} ?y.
        ?x wdt:{relation2} ?z.
        ?z wdt:{relation3} ?y.
        }}
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        count = results['results']['bindings'][0]['count']['value']
        return count

    result = check_implication(relation1, relation2, relation3)
    print(f"Le nombre de sujet qui possède les {relation1} et {relation2} avec impliquation de la relation {relation3} est : {result}")

    return result
# fin de la fonction 7



def getSupportParseur(rule: str):
    """
    Obtient le nombre de situations où les relations dans le corps d'une règle de clause de Horn impliquent la relation dans la tête.

    Args:
        rule (str): La règle de clause de Horn au format "rel1(arg1Left, arg1Right), rel2(arg2Left, arg2Right) => head(argLeft, argRight)"

    Returns:
        int: Le nombre de situations où les relations dans le corps impliquent la relation dans la tête.
    """
    def check_implication(body_atoms, head_atom):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        
        # Construire la partie WHERE de la requête SPARQL
        where_clause = ""
        variables = {}
        for i, atom in enumerate(body_atoms):
            var_left = f"?{atom.argumentLeft}"
            var_right = f"?{atom.argumentRight}"
            if atom.argumentLeft not in variables:
                variables[atom.argumentLeft] = var_left
            if atom.argumentRight not in variables:
                variables[atom.argumentRight] = var_right
            where_clause += f"{var_left} wdt:{atom.relation} {var_right} .\n"
        
        # Ajouter la tête de la clause
        head_var_left = f"?{head_atom.argumentLeft}"
        head_var_right = f"?{head_atom.argumentRight}"
        if head_atom.argumentLeft not in variables:
            variables[head_atom.argumentLeft] = head_var_left
        if head_atom.argumentRight not in variables:
            variables[head_atom.argumentRight] = head_var_right
        where_clause += f"{head_var_left} wdt:{head_atom.relation} {head_var_right} .\n"
        
        query = f"""
        SELECT (COUNT(?x) AS ?count)
        WHERE {{
        {where_clause}
        }}
        """
        
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        count = results['results']['bindings'][0]['count']['value']
        return count

    # Utiliser le parser pour obtenir les atomes du corps et de la tête
    body_atoms, head_atom = parse_horn_clause(rule)
    count = check_implication(body_atoms, head_atom)
    print(f"Le nombre de situations où les relations dans le corps impliquent la relation dans la tête est : {count}")

    return count

# fin de la fonction 7 avec parseur

def headCoverege(relation1, relation2, relation3):
    """
    Savoir le taux en poucentage pour lequel la fonction 7 renvoie True pour des relations particulières.

    Args:
        relation1 (str): La première relation.
        relation2 (str): La deuxième relation.
        relation3 (str): La troisième relation.

    Returns:
        float: La couverture de tête, ou un message d'erreur si le dénominateur est zéro.
    """
    # Obtenir les résultats des fonctions externes
    support_count = int(getSupport(relation1, relation2, relation3))
    num_tuples = int(getNumTuples(relation1))

    if num_tuples == 0:
        return "Division by zero error"

    division_result = support_count / num_tuples
    print("\n", "Le résultat est de : ", division_result)
    return division_result

# fin de la fonction 8



def getConfidence(relation1, relation2, relation3):
    """
    Donne le pourcentage réele entre entre 2 relation avec implication et 2 relation sans implication.

    Args:
        relation1 (str): La première relation.
        relation2 (str): La deuxième relation.
        relation3 (str): La troisième relation.
    """
    support = int(getSupport(relation1, relation2, relation3))
    lose = int(getLose(relation1, relation2))

    if lose != 0:
        confidence = support / lose
        print(f"Le résultat est de : {confidence}")
    else:
        print("Erreur : Division par zéro. Le dénominateur est zéro.")

# fin de la fonction 9



def getLose(relation1, relation2):
    """
    Obtient le nombre de situations où deux relations sont impliquées.

    Args:
        relation1 (str): La première relation.
        relation2 (str): La deuxième relation.

    Returns:
        int: Le nombre de situations où les deux relations sont impliquées.
    """
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

    result = check_implication(relation1, relation2)
    print(f"Le nombre de sujets qui possède les relation {relation1} et {relation2} sans implication est : {result}")

    return result

# fin de la fonction 10



def getAnotherSupport(relation1, relation2, relation3):
    """
    Obtient le nombre de situations où deux relations impliquent une troisième relation, avec une entité différente pour la toisième relation.

    Args:
        relation1 (str): La première relation.
        relation2 (str): La deuxième relation.
        relation3 (str): La troisième relation.

    Returns:
        int: Le nombre de situations où les deux premières relations impliquent la troisième.
    """
    def check_implication(relation1, relation2, relation3):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        query = f"""
        SELECT (COUNT(?x) AS ?count)
        WHERE {{
        ?x wdt:{relation1} ?y.
        ?x wdt:{relation2} ?z.
        ?z wdt:{relation3} ?w.
        }}
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        count = results['results']['bindings'][0]['count']['value']
        return count

    result = check_implication(relation1, relation2, relation3)
    print(f"Le nombre de sujet qui possède les {relation1} et {relation2} avec impliquation de la relation {relation3} est : {result}")

    return result

# fin de la fonction 11



def download_csv():
    """
    Télécharge le fichier CSV contenant les données.

    Utilise tkinter pour demander à l'utilisateur où enregistrer le fichier.
    """
    csv_file = 'data.csv'
    # Utiliser tkinter pour demander à l'utilisateur où enregistrer le fichier
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        shutil.copyfile(csv_file, file_path)
        print(f"Fichier CSV téléchargé à l'emplacement : {file_path}")

# fin de la fonction 2