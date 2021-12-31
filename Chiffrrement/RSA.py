import SHA256
from Algorithme import Inverse
from Algorithme import Premier


class Signature:
    m = ''

    def __init__(self, message):
        m = message

    def chiffre_RSA(self, cle, n):
        c = pow(self.m, cle) % n
        return c

    def dechiffre_RSA(self, cle, n):
        d = pow(self.m, cle) % n
        return d
