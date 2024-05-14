import pandas as pd
import csv
import sqlite3

file_name = "wiki/data/Wikidata_Database_reports_List_of_properties_all_1.csv"
data = pd.read_csv(file_name) 



def creer_table_sqlite(file_name, nom_table, connexion):
    # Vérifier si la table existe déjà
    cursor = connexion.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nom_table}'")
    table_existante = cursor.fetchone()
    
    # Si la table existe déjà, ne rien faire0
    if table_existante:
        print("La table existe déjà.")
        return
    
    # Si la table n'existe pas, procéder à sa création
    with open(file_name, 'r', newline='') as csvfile:
        lecteur_csv = csv.reader(csvfile)
        colonnes = next(lecteur_csv)
        requete_creation_table = f"CREATE TABLE {nom_table} ({', '.join([f'{colonne} TEXT' for colonne in colonnes])})"
        connexion.execute(requete_creation_table)
        for ligne in lecteur_csv:
            requete_insertion = f"INSERT INTO {nom_table} VALUES ({', '.join(['?' for _ in colonnes])})"
            connexion.execute(requete_insertion, ligne)
    
    connexion.commit()

def afficher_ligne_par_numero(nom_table, numero_ligne, connexion):
    cursor = connexion.cursor()
    requete_recherche_ligne = f"SELECT * FROM {nom_table} WHERE ID = ?"
    cursor.execute(requete_recherche_ligne, (numero_ligne,))
    ligne = cursor.fetchone()
    return ligne

# Se connecter à la base de données SQLite
connexion_sqlite = sqlite3.connect('ma_base_de_donnees.db')

# Demander à l'utilisateur de saisir un numéro de ligne
numero_ligne = input("Veuillez entrer le numéro de la ligne que vous souhaitez afficher (entre P6 et P12615) (attention il peut y avoir des numéros qui ne correspondent a aucune ligne): ")

# Nom de la table SQL
nom_table_sql = 'ma_table'

# Afficher la ligne correspondante
ligne = afficher_ligne_par_numero(nom_table_sql, numero_ligne, connexion_sqlite)
if ligne:
    print("Ligne correspondante :")
    print(ligne)
else:
    print("Aucune ligne correspondante pour le numéro donné.")

# Fermer la connexion à la base de données
connexion_sqlite.close()