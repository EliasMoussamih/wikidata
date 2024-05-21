from SPARQLWrapper import SPARQLWrapper, JSON

# Définir l'endpoint SPARQL (par exemple, Wikidata)
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Définir la requête SPARQL
query = """
SELECT (COUNT(distinct ?x) AS ?count)
WHERE {
  ?x wdt:P31 ?y.
  ?x wdt:P6 ?z.
}
"""

# Configurer l'objet SPARQLWrapper
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Exécuter la requête et obtenir les résultats
results = sparql.query().convert()

# Extraire et afficher le résultat
count = results['results']['bindings'][0]['count']['value']
print(f"Count: {count}")
