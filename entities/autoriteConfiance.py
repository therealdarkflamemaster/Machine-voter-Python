# Autorite de Confiance est une autorite pour validation de certificats de tous les serveurs
import Chiffrrement.ElGamal as elgamal
import colorama
from colorama import Fore
from colorama import Style
from entities.Trustee import Trustee

Trustee = Trustee()


def singleton(classe):
    _instance = {}

    def inner():
        if classe not in _instance:
            _instance[classe] = classe()
        return _instance[classe]

    return inner


@singleton
class AutoriteConfiance:
    # we need to check if the message send by users is exactly the message set here (like the verification of the
    # certificates)
    message_admin = "Server-Administration"
    message_serveur = "Server-Serveur"
    message_enregistrement = "Server-Enregistrement"
    message_trustee = "private_key_of_trustee"
    keys_admin = []
    keys_serveur = []
    keys_enregistrement = []

    def set_all_certificats(self):
        self.keys_admin = elgamal.generate_keys()
        self.keys_serveur = elgamal.generate_keys()
        self.keys_enregistrement = elgamal.generate_keys()

    def send_publicKey_admin(self):
        return self.keys_admin["publicKey"]

    def send_publicKey_serveur(self):
        return self.keys_serveur["publicKey"]

    def send_publicKey_enregistrement(self):
        return self.keys_enregistrement["publicKey"]

    def check_certificate_admin(self, cipher):
        plaintext = elgamal.decrypt(self.keys_admin["privateKey"], cipher)
        if plaintext != self.message_admin:
            raise "Server Administartion is not qualified !"

        print(Fore.GREEN + Style.BRIGHT + "Server Administration's certificate has been checked !" + Style.RESET_ALL)

    def check_certificate_serveur(self, cipher):
        plaintext = elgamal.decrypt(self.keys_serveur["privateKey"], cipher)
        if plaintext != self.message_serveur:
            raise "Server Serveur is not qualified !"

        print(Fore.GREEN + Style.BRIGHT + "Server Serveur's certificate has been checked !" + Style.RESET_ALL)

    def check_certificate_enregistrement(self, cipher):
        plaintext = elgamal.decrypt(self.keys_enregistrement["privateKey"], cipher)
        if plaintext != self.message_enregistrement:
            raise "Server Enregistrement is not qualified !"

        print(Fore.GREEN + Style.BRIGHT + "Server Enregistrement's certificate has been checked !" + Style.RESET_ALL)

    def check_keys_trustee(self, cipher):
        plaintext = elgamal.decrypt(Trustee.send_private_key(), cipher)
        if plaintext != self.message_trustee:
            raise "Trustees are not qualified !"

        print(Fore.GREEN + Style.BRIGHT + "Trustees have been checked !" + Style.RESET_ALL)