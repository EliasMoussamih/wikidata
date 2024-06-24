from functions import *

def main():
    print("1. Savoir combien d'entités dans une relation \n" , 
          "2. Télécharger le fichier csv \n",
          "3. Savoir combien d'entités ont deux relations particulières \n",
          "4. Savoir si un élément a plusieurs fois la même relation \n",
          "5. Savoir le nombre de tuples liés par une relation \n",
          "6. Calcule le rapport entre le nombre d'entités distinctes et le nombre de tuples pour une relation donnée \n",
          "7. Savoir dans combien de cas deux relations en impliquent une troisème \n",
          "77. La fonction 7 avec parseur atoms \n",
          "8. Savoir le taux en poucentage pour lequel la fonction 7 renvoie True pour des relations particulières ",
          "9. Donne le pourcentage réele entre entre 2 relation avec implication et 2 relation sans implication \n",
          "10. Savoir dans combien de cas un sujet posséde ces deux relations\n",
          "11. Savoir dans combien de cas deux relations en impliquent une troisème qui est en liaison avec un autre objet\n",
          )

    choice = input("Choisissez une option : ")

    if choice == '1':
        getDomainCardinality("P6")#chef de gouvernement
    elif choice == '2':
        download_csv()
    elif choice == '3':
        getCoocurence("P6", "P26")#chef de gouvernement, mariée
    elif choice == '4':
        getFunctionnalDependencies("Q76", "P40")#Barack Obama, enfant
    elif choice == '5':
        getNumTuples("P40")# enfant
    elif choice == '6':
        fun("P40")# enfant
    elif choice == '7':
        getSupport("P25","P26","P22")# mère , mariée, père
    elif choice == '77':                                     #Avec parseur body_atoms/ head_atoms
        rule = "mother(m,c), spouse(m,f) => father(f,c)"
        getSupportParseur(rule)
    elif choice == '8':
        headCoverege("P25","P26","P22")# mère , mariée, père
    elif choice == '9':
        getConfidence("P25","P26","P22")# mère , mariée, père
    elif choice == '10':
        getLose("P25","P26")# mère , mariée
    elif choice == '11':
        getAnotherSupport("P25","P26","P22")# mère , mariée, père
    else:
        print("Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    main()
