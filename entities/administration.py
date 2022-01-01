# A : représente l’autorité d’administration de l’élection. 选举机构
import pandas as pd
import colorama
from colorama import Fore
from colorama import Style
from entities.Trustee import Trustee
from entities.enregistrement import Enregistrement
from entities.serveur import Serveur
from Chiffrrement.pythonSHA256 import generate_hash
import datetime
import Chiffrrement.ElGamal as elgamal
from Chiffrrement.groupe import prime_bulletin, g_bulletin
from Algorithme.FastPower import pow_mod, myPow, fastExpMod


Trustee = Trustee()
Enregistrement = Enregistrement()
Serveur = Serveur()


def singleton(classe):
    _instance = {}

    def inner():
        if classe not in _instance:
            _instance[classe] = classe()
        return _instance[classe]

    return inner


@singleton
class Administration:
    # certificate is the public Key of the ElGamal, which is used for playing role of verification the identity of the
    # server
    certificate = "Server-Administration"
    certificate_publicKey = []
    info_voter = []  # in format DataFrame
    list_pubCn = []  # liste L dans le docu
    key_public = ""
    info_D = {}

    def set_certificate(self, publicKey):
        self.certificate_publicKey = publicKey

    def send_certificate(self):
        message = self.certificate
        return elgamal.encrypt(self.certificate_publicKey, message)

    def initialElect(self):
        # Un éléction est initialisée sur le serveur A en lui fournissant (par exemple par Ti) la liste des utilisateurs
        # V1...VN (nom, prénom, adresse email).
        self.info_voter = Trustee.getInfos_voteur()
        # A ajoute à cette liste un uuid (Unique User ID) pour chaque utilisateur et fournit cette liste au serveur E.
        # we used the first name and the family name to create a string in methode of SHA256
        self.info_voter['uuid'] = self.info_voter.apply(self.generate_uuid, axis=1)
        print(Fore.GREEN + Style.DIM + "All the uuids of users have been generated " + Style.RESET_ALL)
        Enregistrement.getInfo_voters(self.info_voter)

    def get_all_infos_voters(self):
        return self.info_voter

    def generate_uuid(self, x):
        return generate_hash(x.nom + x.prenom).hex()

    def get_list(self, list_pubcn):
        self.list_pubCn = list_pubcn

    def ask_for_key_public(self):
        self.key_public = Trustee.generate_key_public()

    def generate_election_D(self, candidates_names):
        election_nom = "ELECTION-GS15-A21-LSX-ZXY"
        times = [datetime.date.today()]
        self.info_D = {
            "election_name": election_nom,
            "candidates": candidates_names,
            "times": str(times),
            "public_key": str(self.key_public.p) + " " + str(self.key_public.g) + str(self.key_public.h),
            "list": self.list_pubCn[:3],
            "buttetins": [],
            "result": "not finish yet..."
        }

    def send_election_D(self):
        Serveur.receive_infos_from_a(self.list_pubCn, self.info_voter, self.info_D)

    def get_election_D(self):
        return self.info_D
