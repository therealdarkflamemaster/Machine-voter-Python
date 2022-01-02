# this file (class) is used to create the Cn and the related Pub(Cn)
from Algorithme.Shuffle import shuffle
from Chiffrrement.PBKDF2 import pbkdf2
from Chiffrrement.groupe import g, q, p
from Algorithme.FastPower import pow_mod, fastExpMod


class Credential:
    cn = ""
    pubcn = ""
    chars = "1 2 3 4 5 6 7 8 9 A B C D E F G H J K L M N P Q R S T U V W X Y Z a b c d e f g h i j k m n o p q r s t " \
            "u v w x y z".split()

    chars_origin = "1 2 3 4 5 6 7 8 9 A B C D E F G H J K L M N P Q R S T U V W X Y Z a b c d e f g h i j k m n o p q " \
                   "r s t u v w x y z".split()

    def __init__(self):
        pass

    def get_cn(self):
        self.generate_random_cn()
        return "".join(self.cn)

    def generate_random_cn(self):
        """The first 14 characters are random, and the last one is a checksum to detect typing errors. To
        compute the checksum, each character is interpreted as a base 58 digit: 1 is 0, 2 is 1, . . . , z is
        57. The first 14 characters are interpreted as a big-endian number c1 The checksum is 53 − c1
        mod 53."""
        shuffle(self.chars)
        first_part = self.chars[:14]
        sum = 0
        for char in first_part:
            count = 0
            for ch in self.chars_origin:
                if ch == char:
                    sum += count
                    break
                else:
                    count += 1

        # number checksum
        second_num = (53 - sum) % 53
        while second_num < 0:
            second_num += 58

        second_part = self.chars_origin[second_num]
        self.cn = first_part.append(second_part)
        self.cn = first_part

    def generate_pubcn(self, cn, uuid):
        if cn == "":
            raise "Yous should first generate the Cn"
        """
        From this string, a secret exponent s = secret(c) is derived by using PBKDF2 (RFC 2898)
        with:
        • c as password;
        • HMAC-SHA256 (RFC 2104, FIPS PUB 180-2) as pseudorandom function;
        • the uuid of the election as salt;
        • 1000 iterations
        """
        c = cn.encode('ASCII')
        salt = uuid.encode('ASCII')
        dklen = 256
        """
        Enfin le code de vote est obtenu en calculant Pub(cn) = gs avec g un élément générateur d’un corps fini
        qui est publiquement connu
        """
        a = pbkdf2(c, salt, dklen)
        a = int.from_bytes(a, "big")
        p_int = int(p)
        s = a % p_int
        self.pubcn = hex(fastExpMod(g, s, p_int))
        return self.pubcn
