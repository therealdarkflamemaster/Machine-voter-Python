import math
from Chiffrrement.groupe import q, g
from Chiffrrement.HmacSHA256 import hashed_mac

import struct


def _pbkdf2(password, salt, count, dk_length):
    """
        digestmod
            a crypographic hash constructor, such as hashlib.sha256
            which will be used as an argument to the hmac function.
            Note that the performance difference between sha1 and
            sha256 is not very big. New applications should choose
            sha256 or better.
        password
            The arbitrary-length password (passphrase) (bytes)
        salt
            A bunch of random bytes, generated using a cryptographically
            strong random number generator (such as os.urandom()). NIST
            recommend the salt be _at least_ 128bits (16 bytes) long.
        count
            The iteration count. Set this value as large as you can
            tolerate. NIST recommend that the absolute minimum value
            be 1000. However, it should generally be in the range of
            tens of thousands, or however many cause about a half-second
            delay to the user.
        dk_length
            The lenght of the desired key in bytes. This doesn't need
            to be the same size as the hash functions digest size, but
            it makes sense to use a larger digest hash function if your
            key size is large.
    """

    def pbkdf2_function(pw, salt, count, i):
        # in the first iteration, the hmac message is the salt
        # concatinated with the block number in the form of \x00\x00\x00\x01
        # r = u = hmac.new(pw, salt + struct.pack(">i", i), digestmod).digest()
        r = u = hashed_mac(pw, salt + struct.pack(">i", i))
        for i in range(2, count + 1):
            # in subsequent iterations, the hmac message is the
            # previous hmac digest. The key is always the users password
            # see the hmac specification for notes on padding and stretching
            # u = hmac.new(pw, u, digestmod).digest()
            u = hashed_mac(pw, u)
            # this is the exclusive or of the two byte-strings
            r = bytes(i ^ j for i, j in zip(r, u))
        return r

    dk, h_length = b'', 256
    # we generate as many blocks as are required to
    # concatinate to the desired key size:
    blocks = (dk_length // h_length) + (1 if dk_length % h_length else 0)
    for i in range(1, blocks + 1):
        dk += pbkdf2_function(password, salt, count, i)
    # The length of the key wil be dk_length to the nearest
    # hash block size, i.e. larger than or equal to it. We
    # slice it to the desired length before returning it.
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

