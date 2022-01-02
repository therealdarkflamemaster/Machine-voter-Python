import colorama
from colorama import Fore
from colorama import Style
from Chiffrrement.groupe import prime_bulletin, g_bulletin
from Algorithme.FastPower import pow_mod, fastExpMod
import random
from Chiffrrement.pythonSHA256 import generate_hash


class Bulletin:
    election_id = "ELECTION-GS15-A21-LSX-ZXY"
    uuid = ""
    cn = ""
    choice_chiffre = ""
    zero_knowledge_proof = ""
    # chal_value and resp are two paras need to be used to check the hash value after
    chal_value = 0
    resp = 0
    A = 0

    def __init__(self, cn, uuid, choice_chiffre):
        self.cn = cn
        self.uuid = uuid
        self.choice_chiffre = choice_chiffre

    def generate_zero_knowledge_proof(self, pub_cn):
        # follows the instructions of the new version (generate the Zero Knowledge Proof)
        w = random.randint(1, (prime_bulletin - 1) // 2)
        A = fastExpMod(g_bulletin, w, prime_bulletin)
        # need to take part of cn, or the result will be influenced by the limit of Number in python
        cn = self.cn.encode('ASCII')[:10]
        # S = Pub(Cn)
        S = pub_cn
        M = '||'
        message = str(S) + M + str(A)
        self.A = A
        # need to take part of chal, or the result will be influenced by the limit of Number in python
        hash_message = generate_hash(message)
        self.zero_knowledge_proof = hash_message.hex()
        chal = hash_message[:10]
        cn_value = int.from_bytes(cn, "big") % prime_bulletin
        self.chal_value = int.from_bytes(chal, "big") % prime_bulletin
        self.resp = w - cn_value * self.chal_value % prime_bulletin

    # use to recalculate the value of chal(SHA256), need to check if the user knows his or her Cn
    def return_public_keys(self):
        return [self.chal_value, self.resp]

    def print_infos(self):
        print(Fore.MAGENTA + Style.BRIGHT + "<--- HASH Message: " + str(self.zero_knowledge_proof) + " --->" + Style.RESET_ALL)

    def verify_pub_cn(self, list):
        has_pub_cn = False
        list_message = []
        for pub_cn in list:
            M = '||'
            message = str(pub_cn) + M + str(self.A)
            list_message.append(generate_hash(message).hex())

        for message_temp in list_message:
            if self.zero_knowledge_proof == message_temp:
                has_pub_cn = True
                break

        return has_pub_cn

    def get_zero_knowledge_proof(self):
        return self.zero_knowledge_proof
