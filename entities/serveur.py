# S : est le serveur de vote, celui sur lesque les électeur mettent leur bulletin. 投票服务器
import colorama
from colorama import Fore
from colorama import Style
from entities.Trustee import Trustee
import Chiffrrement.ElGamal as elgamal
from entities.bulletin import Bulletin
from Chiffrrement.BlowFish import input_string, return_string
from Chiffrrement.groupe import prime_bulletin, g_bulletin
from Algorithme.FastPower import pow_mod, myPow, fastExpMod
from Chiffrrement.pythonSHA256 import generate_hash

Trustee = Trustee()


def singleton(classe):
    _instance = {}

    def inner():
        if classe not in _instance:
            _instance[classe] = classe()
        return _instance[classe]

    return inner


@singleton
class Serveur:
    # certificate is the public Key of the ElGamal, which is used for playing role of verification the identity of the
    # server
    certificate = "Server-Serveur"
    certificate_publicKey = []
    list = []
    # in format DataFrame
    info_voter = []
    info_D = {}
    list_bulletin = []

    def set_certificate(self, publicKey):
        self.certificate_publicKey = publicKey

    def send_certificate(self):
        message = self.certificate
        return elgamal.encrypt(self.certificate_publicKey, message)

    def receive_infos_from_a(self, list, info_voter, info_D):
        self.info_D = info_D
        self.info_voter = info_voter
        self.list = list
        print(Fore.GREEN + Style.DIM + "Server S get all infos in phase 1" + Style.RESET_ALL)

    def check_bulletin_and_add(self, voter_this_pub_cn, voter_this_cn, uuid, choice_chiffre):
        bulletin_temp = Bulletin(return_string(voter_this_pub_cn), return_string(voter_this_cn), return_string(uuid),
                                 return_string(choice_chiffre))
        # Le bulletin contient également une signature qui fait office de zero-knowledge proof permettant de prouver
        # que le bulletin a été rempli et signé par celui qui connait cn
        bulletin_temp.generate_zero_knowledge_proof()
        # le serveur de vote verifie la validite du vote
        # 1. le code existe dans la liste
        # 2. en demandant la preuve de la connaissance de Cn
        pub_cn = return_string(voter_this_pub_cn)
        uuid = return_string(uuid)
        bool_exist = pub_cn in self.list
        if not bool_exist:
            return "The Pub_Cn is not in the list registered in the server"

        zero_knowledge_proof = bulletin_temp.zero_knowledge_proof
        # 2. en demandant la preuve de la connaissance de Cn
        [chal_value, resp] = bulletin_temp.return_public_keys()
        # to test if chal = hash...
        # to use the uuid of user to find the right Cn
        info_voter = self.info_voter
        cn_right = info_voter[info_voter["uuid"] == uuid]["cn"].tolist()
        cn_right = cn_right[0]
        cn_right = cn_right.encode('ASCII')[:10]
        cn_value = int.from_bytes(cn_right, "big") % prime_bulletin
        Pcn = fastExpMod(g_bulletin, cn_value, prime_bulletin)
        b1 = fastExpMod(Pcn, chal_value, prime_bulletin)
        b2 = fastExpMod(g_bulletin, resp, prime_bulletin)
        A = b1 * b2 % prime_bulletin
        S = pub_cn
        M = '||'
        message = str(S) + M + str(A)
        # need to take part of chal, or the result will be influenced by the limit of Number in python
        chal_temp = generate_hash(message)[:10]
        chal_value_temp = int.from_bytes(chal_temp, "big") % prime_bulletin
        ##########################################################################################################
        ################################# "The 'user' seems do not know his Cn"
        if chal_value_temp == chal_value:
            self.list_bulletin.append(bulletin_temp)
            return "Add bulletin successfully"
        else:
            return "The 'user' seems do not know his Cn"

    def get_all_bulletins(self):
        return self.list_bulletin

    def phase_depouillement(self):
        candidates = self.info_D["candidates"]
        result = {}
        # initialisation
        for candidate in candidates:
            result[candidate] = 0

        for bulletin in self.list_bulletin:
            choice_chiffre = bulletin.choice_chiffre
            choice = Trustee.decrypt_choice(choice_chiffre)
            result[choice] += 1

        winner = ""
        max_vote = 0
        for candidate in candidates:
            if result[candidate] > max_vote:
                max_vote = result[candidate]
                winner = candidate

        self.info_D["result"] = {
            "pouillement": str(result),
            "winner": winner
        }
        return self.info_D
