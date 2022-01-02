import math
from Chiffrrement.groupe import q, g
from Chiffrrement.HmacSHA256 import hashed_mac

import struct


def _pbkdf2(password, salt, count, dk_length):
    """
        digestmod
            with sha256
        password
            in format bytes
        salt
            A bunch of random bytes
        count
            The iteration count. 1000
        dk_length
            The length of the desired key in bytes. 
    """

    def pbkdf2_function(pw, salt, count, i):
        
        r = u = hashed_mac(pw, salt + struct.pack(">i", i))
        for i in range(2, count + 1):
            # in subsequent iterations, the hmac message is the
            # previous hmac digest.
            u = hashed_mac(pw, u)
            # the exclusive or of the two byte-strings
            r = bytes(i ^ j for i, j in zip(r, u))
        return r

    dk, h_length = b'', 256
    # generate as many blocks as are required to
    # concatinate to the desired key size:
    blocks = (dk_length // h_length) + (1 if dk_length % h_length else 0)
    for i in range(1, blocks + 1):
        dk += pbkdf2_function(password, salt, count, i)
    # The length of the key wil be dk_length to the nearest
    # hash block size
    return dk[:dk_length]


def pbkdf2(passphrase, salt, key_length, iterations=1000):
    return _pbkdf2(passphrase, salt, iterations, key_length)



# c = 'oTwED3nN8hkuPi1'.encode('ASCII')
# salt = '185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969'.encode('ASCII')
# dklen = 256
#
# a = pbkdf2(c, salt, dklen)
# a = int.from_bytes(a, "big")
# q = int(q)
# s = a % q
# pubcn = fast_power(g, s)
# print(s)
# print(pubcn)

