from Chiffrrement import SHA256

class zeroKnowlwdge:

    def __init__(self,premier,generateur,signature,message):
        p=premier
        g=generateur
        w = random(1, self.p - 1)
        chal = ''
        s=signature
        m=message
        a = pow(self.g, w)


    def get_w(self):
        return self.w

    def challenge(self):
        sha=SHA256()
        self.chal=sha(self.s+self.m+a)
        return self.chal

    #v,c''est quoi???
    def verifier(self, pub, v, resp):
        a=pow(self.g, resp)*pow(v, self.chal)
        ver=SHA256(self.s+self.m+a)
        if(self.chal==ver):
            print("Verifie")
        else:
            print("Pas verifie")
