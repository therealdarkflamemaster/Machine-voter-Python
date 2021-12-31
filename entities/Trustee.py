# T1,...,TI : sont les i utilisateurs de confiance chargées du dépouillement. 负责点票的用户
import pandas as pd
import colorama
from colorama import Fore
from colorama import Style
import random
import Chiffrrement.ElGamal as elgamal
from Chiffrrement.groupe import q, g
from Algorithme.FastPower import pow_mod


def singleton(classe):
    _instance = {}

    def inner():
        if classe not in _instance:
            _instance[classe] = classe()
        return _instance[classe]

    return inner


@singleton
class Trustee(object):
    # private key(s) of all Trustee
    private_message = "private_key_of_trustee"
    # register in form DataFrame
    info_voter = pd.DataFrame(columns=('nom', 'prenom', 'mail'))
    # register in form list
    voters = []
    numbers_s = []
    number_sum_s = 0
    privateKey = None
    publicKey = None

    def __init__(self):
        pass

    def init(self):
        pass

    def generate_keys(self):
        # we use one Trustee as a server, but we generate 5 Si belonging to Zp to keep the principe of the document
        prime_alea = elgamal.find_prime(256, 32)
        # we use this prime aleatoire to find all the numbers of 5 Si
        for i in range(5):
            number_si = random.randint(1, (prime_alea - 1) // 2)
            self.numbers_s.append(number_si)
            self.number_sum_s += number_si

        # p is the prime
        # g is the primitve root
        # x is random in (0, p-1) inclusive
        # h = g ^ x mod p
        g = elgamal.find_primitive_root(prime_alea)
        g = elgamal.modexp(g, 2, prime_alea)
        h = elgamal.modexp(g, self.number_sum_s, prime_alea)
        iNumBits = 256
        self.publicKey = elgamal.PublicKey(prime_alea, g, h, iNumBits)
        self.privateKey = elgamal.PrivateKey(prime_alea, g, self.number_sum_s, iNumBits)

    def send_public_key(self):
        return self.publicKey

    def addInfo_voteur(self, nom, prenom, mail, voter):
        self.info_voter = self.info_voter.append([{'nom': nom, 'prenom': prenom, 'mail': mail}])
        self.voters.append(voter)
        # print(Fore.GREEN + Style.DIM + "Add " + nom + " successfully for Trustee !" + Style.RESET_ALL)

    def getInfos_voteur(self):
        return self.info_voter

    def get_voters(self):
        return self.voters

    # need to change, how to generate the key public
    def generate_key_public(self):
        # Le serveur A demande aux utilisateurs chargé du dépouillement Ti de lui communiquer une clé publique ai.
        return self.publicKey

    # Durant le vote, une des personnes en charge du dépouillement T1, ..., TI peut s’assurer de l’intégrité des
    # votes. (Phase d'audit)
    def assure_integrity(self, bulletins, list):
        print(Fore.BLUE + Style.DIM + "<--------------- Phase d'audit starts --------------------->" + Style.RESET_ALL)
        # 1. chaque bulletin contient une signature qui prouve la connaissance d'un des codes de vote Pub(Cn)
        # bulletins_codes is a list to restore all the pub_cns codes in it, which is used for the second verification

        #    we have to generate a list with all the pub(Cn)s, this will be a list of all the hash256 values of the
        #    message similar to those of Zero-Knowledge-Proof
        #    The origin Zero-Knowledge-Proof has used the Pub(Cn) as the value 'S', so in this way, we can test the
        #    presence of Pub(Cn) in the message hash256

        bulletins_codes = []

        for bulletin in bulletins:
            bool_has = bulletin.verify_pub_cn(list)
            if not bool_has:
                return "Trustee has scanned a vote unqualified !"
            bulletins_codes.append(bulletin.get_zero_knowledge_proof())

        print(Fore.GREEN + Style.BRIGHT + "Trustee has checked all the bulletins, each one has a prove of Pub(Cn)"
              + Style.RESET_ALL)
        # 2. ... que chaque bulletin correspond a la signature associee a un code (Pub(Cn)) de vote distinct
        set_bulletins = set(bulletins_codes)
        if len(set_bulletins) == len(bulletins_codes):
            print(Fore.GREEN + Style.BRIGHT + "Trustee has checked each bulletin has a different Pub(Cn) from one "
                                              "another" + Style.RESET_ALL)
        else:
            return "Trustee has checked there are 2 bulletins with same bulletin !"

        return "<--------------- Audit Phase finish --------------------->"

    def send_private_key(self):
        return self.privateKey

    # this function is used to test the validity of Trustee in the phase depouillement
    def send_cipher_message(self):
        message = self.private_message
        return elgamal.encrypt(self.publicKey, message)

    def decrypt_choice(self, choice_chiffre):
        return elgamal.decrypt(self.privateKey, choice_chiffre)