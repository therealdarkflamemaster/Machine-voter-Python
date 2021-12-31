import random
import pandas as pd
import sys
import colorama
from colorama import Fore
from colorama import Style
from entities.Voteur import Voteur
from entities.Trustee import Trustee
from entities.administration import Administration
from entities.enregistrement import Enregistrement
from entities.autoriteConfiance import AutoriteConfiance
from entities.serveur import Serveur
from functions import print_choices, register_un_electer, create_a_vote, register_a_vote, register_a_final_vote, \
    verify_a_vote
from Chiffrrement.BlowFish import input_string, return_string

Trustee = Trustee()
Administration = Administration()
Enregistrement = Enregistrement()
Serveur = Serveur()
AutoriteConfiance = AutoriteConfiance()

"""
this election program allows only one voter, with the consideration of the fact that there should 
be one computer for one voter, if not, it will affiche more than one Cn and Pub(Cn) on the screen.

Therefore, to ensure the number of bulletins and the number of voters, I have created 10 voters virtuels
to make sure that there will be a winner for thsi election. 
"""

# voters is a list to store all the voters created by user
voters = []

# candidates is a list pre-created, which is the list of the candidates of this election
# in this, we have written the names of the creators of the this program
candidates = {
    "lsx": 0,
    "zxy": 0
}
# candidates_names are the lists of all candidates' names in this election
candidates_names = list(candidates.keys())

# choix is a list to record all the votes made by the computer so far
choix = []
print(Fore.BLUE + Style.BRIGHT + "Before the election starts, we need to create the certificates for all the servers" +
      " and to create the keys needed of Trustee " + Style.RESET_ALL)
print(Fore.GREEN + Style.DIM + "creating ..." + Style.RESET_ALL)
AutoriteConfiance.set_all_certificats()

# start the procedure of verification the certificates of three servers: Admin, Serveur, Enregistrement

# 1. send all the certificates to the three servers
Administration.set_certificate(AutoriteConfiance.send_publicKey_admin())
Serveur.set_certificate(AutoriteConfiance.send_publicKey_serveur())
Enregistrement.set_certificate(AutoriteConfiance.send_publicKey_enregistrement())

# 2. the user need to receive all the certificates of the three servers
print(Fore.GREEN + Style.BRIGHT + "Now begins to verify all the servers used in this election" + Style.RESET_ALL)
certificate_admin = Administration.send_certificate()
certificate_serveur = Serveur.send_certificate()
certificate_enregistrement = Enregistrement.send_certificate()
AutoriteConfiance.check_certificate_admin(certificate_admin)
AutoriteConfiance.check_certificate_serveur(certificate_serveur)
AutoriteConfiance.check_certificate_enregistrement(certificate_enregistrement)

# 3. Generate all the private key and the global public key of the Trustee
Trustee.generate_keys()
print(Fore.GREEN + Style.BRIGHT + "Trustees are on their positions (Keys have been created !)" + Style.RESET_ALL)

# here we start the election procedure
print(Fore.BLUE + Style.BRIGHT + "Bonjour ô maître! Comme puis-je aider votre Sainteté ?" + Style.RESET_ALL)
# need to create the first voter to start to others phases
# as we concerned, this election will return the Cn and Pub(Cn) to each voter, so as we are on the only side of
# this election, for the moment, we will allow one voter to be created.
print(Fore.BLUE + Style.BRIGHT + "You have to register first yourself as a voter" + Style.RESET_ALL)
voter_this = register_un_electer()
voters.append(voter_this)
print(Fore.GREEN + Style.BRIGHT + "Voter [ " + str(voter_this.nom) + " ] has been created. " + Style.RESET_ALL)
print(Fore.YELLOW + Style.DIM + "All the communications are encrypted with the algorithm BlowFish " + Style.RESET_ALL)
# after the creation of all the voters, we need to have some more voters to keep the election run well
# Phase 0 : creat 10 voters computers
for i in range(10):
    nom = 'voter' + str(i)
    prenom = str(i)
    mail = 'voter' + str(i) + '@email.com'
    voterTemp = Voteur(input_string(nom), input_string(prenom), input_string(mail))

voters = Trustee.get_voters()
# Phase 1 : Mise en place d’une élection
Administration.initialElect()
[voter_this_cn, voter_this_pub_cn] = Enregistrement.sendCn_to_voter(voter_this)
voter_this_cn = return_string(voter_this_cn)
voter_this_pub_cn = return_string(voter_this_pub_cn)
print(Fore.RED + Style.BRIGHT + 'You has got your Cn ' + voter_this_cn + Style.RESET_ALL)
print(Fore.RED + Style.BRIGHT + 'You has got your Pub(Cn) ' + voter_this_pub_cn + Style.RESET_ALL)

# 4. Le serveur E envoie à chacun des utilisateurs Vn son identifiant cn
for voter in voters[1:]:
    cn_encrypted = Enregistrement.sendCn_to_voter(voter)[0]
    cn_temp = return_string(cn_encrypted)
    print(Fore.RED + Style.DIM + voter.nom + ' has got his Cn ' + str(cn_temp) + Style.RESET_ALL)

# 5. Le serveur E envoie la liste des codes de vote L = shuffle (Pub(c1); : : : Pub(cN)) au serveur A
Enregistrement.generate_lists()
Administration.get_list(Enregistrement.send_list())

# 6. Le serveur A demande aux utilisateurs chargé du dépouillement Ti de lui communiquer une clé publique ai.
## 还没有做，需要得到 Vi - Vn 的 公钥和私钥以后再说
Administration.ask_for_key_public()

# 7. Les données de l’élection D sont entrées dans le serveur A ;
Administration.generate_election_D(candidates_names)

# 8. Le serveur A envoie au serveur de vote S la liste des codes de vote L et les données de l’élection
Administration.send_election_D()

# Phase de vote
# Lorsqu’un utilisateur souhaite voter, il se connecte au serveur pour obtenir les données de l’élection.
print(Fore.MAGENTA + Style.BRIGHT + "<-------------YOU HAVE CONNECTED TO THE SERVER------------->" + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "<---------------------INFO ELECTION------------------------>" + Style.RESET_ALL)
info_D = Administration.get_election_D()
for key in info_D:
    if isinstance(info_D[key], list):
        print(Fore.MAGENTA + Style.DIM + key, " : ")
        print(str(info_D[key]), end='\r')
    elif isinstance(info_D[key], str):
        print(Fore.MAGENTA + Style.DIM + key, " : ", info_D[key] + Style.RESET_ALL)
    elif isinstance(info_D[key], dict):
        print(Fore.MAGENTA + Style.DIM + key, " : ", str(info_D[key]) + Style.RESET_ALL)
print(Fore.MAGENTA + Style.BRIGHT + "<---------------------------------------------------------->" + Style.RESET_ALL)
"""
1. You need to vote first (you can vote many times, as you like)
2. Choice between/among all your votes, numbered for 1 to n 
3. your final choice has been registered in the bulletin, and you can no longer change it
4. you can verify your vote by the choice 3
5. the phase depouillement with the choice 4
"""
# variable boolean to know whether the user has made his or her final choice
choice_2 = False

# generate the list of uuids
infos = Administration.get_all_infos_voters()
uuids = infos["uuid"].tolist()


# register the votes results of other computers voters
# use random here
def register_other_votes(candidates_names):
    # use para count to iterate the list UUIDs
    count = 1
    for voter_temp in voters[1:]:
        [voter_cn, voter_pub_cn] = Enregistrement.sendCn_to_voter(voter_temp)
        choix = random.randint(0, 1)
        choice_temp = register_a_final_vote(candidates_names, choix, voter_pub_cn, uuids[count], voter_cn, publicKey)
        count += 1
        candidates[candidates_names[choice_temp]] += 1


while True:
    print(Fore.BLUE + Style.BRIGHT + "Bonjour ô maître " + str(voter_this.nom) + "! Comme puis-je aider votre "
                                                                                 "Sainteté ?" + Style.RESET_ALL)
    print_choices()
    choice = input(Fore.BLUE + Style.BRIGHT + "Please input 1 ~ 4: " + Style.RESET_ALL)
    if choice == '1':
        # when choice_2 == True, means that the user has  already made his or her final decision
        if choice_2:
            print(Fore.BLUE + Style.DIM + "You have already made your final decision, you can now verify your vote or "
                                          "go the audit part." + Style.RESET_ALL)
            continue

        choix_temp = create_a_vote(voters, candidates_names)
        # till now, the para "choix-temp" and "choix" are just the temporary choice before the user's final decision
        #  so that we do not need to send it to the server, but to store it locally
        choix.append(choix_temp)

    if choice == '2':
        # when choice_2 == True, means that the user has  already made his or her final decision
        if choice_2:
            print(Fore.BLUE + Style.DIM + "You have already made your final decision, you can now verify your vote or "
                                          "go the audit part." + Style.RESET_ALL)
            continue

        publicKey = Trustee.send_public_key()
        choice_final = register_a_vote(candidates_names, choix, voter_this_pub_cn, publicKey, uuids[0], voter_this_cn)
        # 比较偏向于 Serveur利用全部的bulletins来计票，而不是在外面统计
        candidates[candidates_names[choice_final]] += 1
        choice_2 = True
        # register the votes results of other computers voters
        register_other_votes(candidates_names)

    if choice == '3':
        # durant la phase de vote, chaque utilisateur doit pouvoir verifier la presence de son bulletin de vote en
        # demandant la liste de signatures de l'ensemble de tous les votes
        bulletins = Serveur.get_all_bulletins()
        verify_a_vote(bulletins)

    if choice == '4':
        # check has the user finish his phase of voting
        if not choice_2:
            print(
                Fore.BLUE + Style.DIM + "You should make your choice to make the election run first !" + Style.RESET_ALL)
        else:
            # Durant le vote, une des personnes en charge du dépouillement T1; : : : ;TI peut s’assurer de l’intégrité des
            # votes. (Phase d'audit)
            bulletins = Serveur.get_all_bulletins()
            statement = Trustee.assure_integrity(bulletins, Enregistrement.send_list())
            print(Fore.BLUE + Style.DIM + statement + Style.RESET_ALL)
            # Phase de depouillement
            """
            Le décompte des votes nécessites l’ensemble des clés privées des personnes en chages du dépouillement.
            On procédera alors au déchiffrement des votes chiffrés et l’on fera simplement la sommes des votes de
            chaque candidats.
            """
            AutoriteConfiance.check_keys_trustee(Trustee.send_cipher_message())
            print(Fore.BLUE + Style.BRIGHT + "Now begins the phase depouillement" + Style.RESET_ALL)
            info_D = Serveur.phase_depouillement()
            for key in info_D:
                if isinstance(info_D[key], list):
                    print(Fore.MAGENTA + Style.DIM + key, " : ")
                    print(str(info_D[key]), end='\r')
                elif isinstance(info_D[key], str):
                    print(Fore.MAGENTA + Style.DIM + key, " : ", info_D[key] + Style.RESET_ALL)
                elif isinstance(info_D[key], dict):
                    print(Fore.MAGENTA + Style.DIM + key, " : ", str(info_D[key]) + Style.RESET_ALL)
            print(Fore.BLUE + Style.BRIGHT + "<---------------------------------------------------------->"
                  + Style.RESET_ALL)
            break

    print(Fore.BLUE + Style.BRIGHT + "<---------------------------------------------------------->" + Style.RESET_ALL)
