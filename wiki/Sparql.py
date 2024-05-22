from SPARQLWrapper import SPARQLWrapper, JSON

# Définir l'endpoint SPARQL (par exemple, Wikidata)
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Définir la requête que l'on veut effectuer
requete = input("Quelle requête voulez vous effectuer ? \n"+
                "Requête de liaison (liaison), requête de relation (rel) \n")


if(requete == "liaison" or requete == "rel"):

  # Définir les relations 
  relation1 = input("Quelle est votre première relation ? (les relations sont entre P6 et P12615) \n"+
                    "Il peut y avoir des numéros qui ne sont liés à aucune relation \n"+
                    "Attention à mettre le P en majuscule \n")
  
  relation2 = input("Quelle est votre deuxième relation ? \n")


else: 

  print("la requête donnée n'existe pas, veuillez donner une requête existante")



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



# Lancer les requêtes SPARQL


if(requete == "liaison"):

  # Configurer l'objet SPARQLWrapper
  sparql.setQuery(liaison)
  sparql.setReturnFormat(JSON)

  # Exécuter la requête et obtenir les résultats
  results = sparql.query().convert()

  # Extraire et afficher le résultat
  count = results['results']['bindings'][0]['count']['value']
  print(f"Count: {count}")


elif(requete == "rel"):

  # Configurer l'objet SPARQLWrapper
  sparql.setQuery(rel1)
  sparql.setReturnFormat(JSON)

  # Exécuter la requête et obtenir les résultats
  results = sparql.query().convert()

  # Extraire et afficher le résultat
  count = results['results']['bindings'][0]['count']['value']
  print(f"Count: {count}")



  # Configurer l'objet SPARQLWrapper
  sparql.setQuery(rel2)
  sparql.setReturnFormat(JSON)

  # Exécuter la requête et obtenir les résultats
  results = sparql.query().convert()

  # Extraire et afficher le résultat
  count = results['results']['bindings'][0]['count']['value']
  print(f"Count: {count}")