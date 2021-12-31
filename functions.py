import colorama
from colorama import Fore
from colorama import Style
from entities.Voteur import Voteur
from entities.administration import Administration
from entities.bulletin import Bulletin
from entities.serveur import Serveur
from Chiffrrement.BlowFish import driver_init, input_string, return_string
import Chiffrrement.ElGamal as elgamal

Serveur = Serveur()

# initialization of the BlowFish
driver_init()


def create_a_vote(voter, candidates):
    print(Fore.BLUE + Style.BRIGHT + "You have chosen [Créer un vote]." + Style.RESET_ALL)
    voter_selected = voter[-1]
    print(Fore.BLUE + Style.BRIGHT + "Please make the choice for the voter " + str(voter_selected.nom) + Style.RESET_ALL)
    number_of_candidates = len(candidates)
    for i in range(number_of_candidates):
        print("<-" + str(i) + "-> " + candidates[i])

    choice = check_input("your choice for the vote" + Style.RESET_ALL)
    print(Fore.GREEN + Style.DIM + "You have selected the " + str(candidates[int(choice)]) + Style.RESET_ALL)
    return int(choice)


def register_un_electer():
    print(Fore.BLUE + Style.BRIGHT + "Now you need to type in the information of this voter" + Style.RESET_ALL)
    nom = check_input(Fore.YELLOW + Style.DIM + "voter's family name"+ Style.RESET_ALL)
    prenom = check_input(Fore.YELLOW + Style.DIM + "voter's first name"+ Style.RESET_ALL)
    email = check_input(Fore.YELLOW + Style.DIM + "voter's email address" + Style.RESET_ALL)
    # with the BlowFish, make sure the transmission is safe
    voterTemp = Voteur(input_string(nom), input_string(prenom), input_string(email))
    return voterTemp


def register_a_vote(candidates_names, choix, voter_this_pub_cn, publicKey, uuid, voter_this_cn):
    print(Fore.BLUE + Style.BRIGHT + "You have chosen [Enregistrer un vote]." + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + "There are the votes you have made :" + Style.RESET_ALL)
    for i in range(len(choix)):
        print(Fore.BLUE + Style.DIM + "<-" + str(i) + "-> " + candidates_names[choix[i]] + " " + Style.RESET_ALL)

    choice_final = check_input("the number of vote you want to register")
    # Il fait son choix, le chiffre en utilisant la clé publique et enregistre son bulletin de vote associée au code de
    # vote Pub(cn).
    choice = str(candidates_names[int(choice_final)])
    choice_chiffre = elgamal.encrypt(publicKey, str(choice))
    print(Fore.GREEN + Style.BRIGHT + "Your choice has been encrypted" + Style.RESET_ALL)
    # use the algo BlowFish to communicate with the Server Vote
    message = Serveur.check_bulletin_and_add(input_string(voter_this_pub_cn), input_string(voter_this_cn),
                                             input_string(uuid), input_string(choice_chiffre))
    print(Fore.GREEN + Style.DIM + message + Style.RESET_ALL)
    print(message)
    return int(choice_final)


# this function is used to generate the bulletins for the computer voters
def register_a_final_vote(candidates_names, choice_final, voter_this_pub_cn, uuid, voter_this_cn, publicKey):
    choice = str(candidates_names[int(choice_final)])
    choice_chiffre = elgamal.encrypt(publicKey, str(choice))
    message = Serveur.check_bulletin_and_add(input_string(voter_this_pub_cn), input_string(voter_this_cn),
                                             input_string(uuid), input_string(choice_chiffre))
    print(Fore.GREEN + Style.DIM + message + " for(uuid) " + str(uuid) + Style.RESET_ALL)
    return int(choice_final)


def verify_a_vote(bulletins):
    print(Fore.BLUE + Style.BRIGHT + "You have chosen [Vérifier un vote]." + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + "----------------------All votes recorded-------------------------" + Style.RESET_ALL)
    for bulletin in bulletins:
        bulletin.print_infos()
    print(Fore.BLUE + Style.BRIGHT + "------------------------------END--------------------------------"+ Style.RESET_ALL)


def print_choices():
    print(Fore.BLUE + Style.BRIGHT + "->1<- Créer un vote.")
    print("->2<- Enregistrer un vote.")
    print("->3<- Vérifier un vote.")
    print("->4<- Procéder au dépouillement." + Style.RESET_ALL)


def check_input(parameter):
    while True:
        res = input(Fore.BLUE + Style.DIM + "Please input " + str(parameter) + " : " + Style.RESET_ALL)
        if len(res) == 0 or res.isspace():
            print(Fore.RED + Style.DIM + str(parameter) + "can't be nul" + Style.RESET_ALL)
        else:
            break

    return res

