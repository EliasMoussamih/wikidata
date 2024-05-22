from SPARQLWrapper import SPARQLWrapper, JSON

# Définir l'endpoint SPARQL (par exemple, Wikidata)
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Définir les relations dont on veut savoir le nombre d'entités communs
relation1 = input("Quelle est votre première relation (les relations sont entre P6 et P12615) \n"+
                  "Il peut y avoir des numéros qui ne sont liés à aucune relation \n"+
                  "Attention à mettre le P en majuscule \n")
relation2 = input("Quelle est votre deuxième relation \n")


# Définir la requête SPARQL
query = f"""
SELECT (COUNT(distinct ?x) AS ?count)
WHERE {{
  ?x wdt:{relation1} ?y.       
  ?x wdt:{relation2} ?z.
}}
"""

# Configurer l'objet SPARQLWrapper
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Exécuter la requête et obtenir les résultats
results = sparql.query().convert()

# Extraire et afficher le résultat
count = results['results']['bindings'][0]['count']['value']
print(f"Count: {count}")
