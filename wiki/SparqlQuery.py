# main.py

from functions import *

def main():
    print("1. Savoir combien d'entités dans une relation \n" , 
          "2. Télécharger le fichier csv \n",
          "3. Savoir combien d'entités ont deux relations particulières \n",
          "4. Savoir si un élément a plusieurs fois la même relation \n",
          "5. Savoir le nombre de tuples liés par une relation \n",
          "6. \n",
          "7. Savoir dans combien de cas deux relations en impliquent une troisème \n",
          "8. \n",
          "9. \n",
          "10. \n",
          "11. \n",
          )

    choice = input("Choisissez une option : ")

    if choice == '1':
        getDomainCardinality("P6")
    elif choice == '2':
        download_csv()
    elif choice == '3':
        getCoocurence("P6", "P26")
    elif choice == '4':
        getFunctionnalDependencies("Q76", "P40")
    elif choice == '5':
        getNumTuples("P40")
    elif choice == '6':
        fun("P40")
    elif choice == '7':
        getSupport("P26","P40","P25")
    elif choice == '8':
        headCoverege("P26","P40","P25")
    elif choice == '9':
        getConfidence("P26","P40","P25")
    elif choice == '10':
        getLose("P26","P40")
    elif choice == '11':
        getAnotherSupport("P26","P40","P25")
    else:
        print("Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    main()
