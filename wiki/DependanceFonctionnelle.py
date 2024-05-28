from SPARQLWrapper import SPARQLWrapper, JSON

# Définir l'endpoint SPARQL (par exemple, Wikidata)
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

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
