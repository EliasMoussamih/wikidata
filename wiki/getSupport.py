from SPARQLWrapper import SPARQLWrapper, JSON

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

if __name__ == "__main__":
    # Demander les relations à l'utilisateur
    relation1 = input("Entrez la première relation (par exemple, P26) : ")
    relation2 = input("Entrez la deuxième relation (par exemple, P40) : ")
    relation3 = input("Entrez la troisième relation (par exemple, P25) : ")

    # Exécuter la fonction et afficher le résultat
    result = check_implication(relation1, relation2, relation3)
    print(f"Le nombre de situations où {relation1} et {relation2} impliquent {relation3} est : {result}")
