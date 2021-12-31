# V1, ..., Vn, ..., VN : sont les voteurs. 投票者
import colorama
from colorama import Fore
from colorama import Style
from Chiffrrement.BlowFish import input_string, return_string
from entities.Trustee import Trustee

Trustee = Trustee()

class Voteur:
    nom = ""
    prenom = ""
    mail = ""
    cn = ""
    pub_cn = ""

    def __init__(self, nom, prenom, mail):
        self.nom = return_string(nom)
        self.prenom = return_string(prenom)
        self.mail = return_string(mail)
        Trustee.addInfo_voteur(self.nom, self.prenom, self.mail, self)

    def set_cn(self, cn):
        self.cn = cn

    def set_pub_cn(self, pub_cn):
        self.pub_cn = pub_cn

