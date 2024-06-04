# main.py

from functions import *

def main():
    print("1. Savoir combien d'entités dans une relation \n" , 
          "2. \n",
          "3. Savoir combien d'entités ont deux relations particulières \n",
          "4. Savoir si un élément a plusieurs fois la même relation \n",
          "5. Savoir le nombre de tuples liés par une relation \n",
          "6. \n",
          "7. Savoir dans combien de cas deux relations en impliquent une troisème \n",
          "8. \n",
          "9. \n",
          "10. \n",
          "11. \n",
          "12. Télécharger le fichier csv")

    choice = input("Choisissez une option : ")

    if choice == '1':
        getDomainCardinality()
    elif choice == '2':
        getCoocurence()
    elif choice == '3':
        getCoocurence()
    elif choice == '4':
        getFunctionnalDependencies()
    elif choice == '5':
        getNumTuples()
    elif choice == '6':
        fun()
    elif choice == '7':
        getSupport()
    elif choice == '8':
        headCoverege()
    elif choice == '9':
        getConfidence()
    elif choice == '10':
        getLose()
    elif choice == '11':
        getAnotherSupport()
    elif choice == '12':
        download_csv()
    else:
        print("Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    main()
