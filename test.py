
# from Chiffrrement.Blowfish import Blowfish
# # uuid
#
# print(uuid.uuid1())
# print(uuid.uuid1())
#
#
# print(generate_hash("abc"))
# print(generate_hash("aac"))

# communication BlowFish
# from Chiffrrement.Credential import Credential
# from Chiffrrement.PBKDF2 import pbkdf2
# from Chiffrrement.groupe import q, g
# from Algorithme.FastPower import pow_mod
#
# credit = Credential()
#
# print(credit.get_cn())
#
# c = 'oTwED3nN8hkuPi1'.encode('ASCII')
# salt = '185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969'.encode('ASCII')
# dklen = 256
#
# a = pbkdf2(c, salt, dklen)
# a = int.from_bytes(a, "big")
# q = int(q)
# s = a % q
# print(s)
# pubcn = pow_mod(g, s, q)
#
# print(hex(pubcn))

# ELGamal Test
import tkinter

import Chiffrrement.ElGamal as elgamal
from Chiffrrement.groupe import q, g
from Algorithme.FastPower import pow_mod, fastExpMod
import random
from Chiffrrement.pythonSHA256 import generate_hash
# keys = elgamal.generate_keys()
# #returns a dictionary {'privateKey': privateKeyObject, 'publicKey': publicKeyObject}
# cipher = elgamal.encrypt(keys["publicKey"], "This is the message I want to encrypt")
# # #returns a string
# plaintext = elgamal.decrypt(keys["privateKey"], cipher)
# print(plaintext)
# # #returns the message passed to elgamal.encrypt()


prime_alea = elgamal.find_prime(256, 32)
g = elgamal.find_primitive_root(prime_alea)
w = random.randint(1, (prime_alea - 1) // 2)
A = fastExpMod(g, w, prime_alea)
print(A)
# need to take part of cn, or the result will be influenced by the limit of Number in python
cn = "jyvkhFaYqJsiDBh".encode('ASCII')[:10]
# S = Pub(Cn)
S = 0x16e87c72630852624a29b1eb5084fa18446db9f12b1467e32bfac38b9418c71e20fb529a91830157d9a8f0ecc3e721f7ac2c03b9e9962cff4b96f38a99a6e85ff5660e850df3831a8e2a42d6a352929d57c9333fd6f6dbf3e6285313706e9bae8fd3e990833df4567878f094322b0a3f5d0fff6bd9cb92518f13e2b6e3b3e694a831732d22fedb709a36cc4f3ce107a570d0e1980e55616a0d95d2f864a5af7f1a888fb5ed3478a345d2b0128184de00970675c24205022595bd104bd0d4ba0927a1468ad9788cbf49a075b81a1e4ec7be2665d9a05827ffeb22cd4e7b5983df5eec199cc4254d807ca63c363e4332e1df2a03ea7f779b52a72bb33323dbb254
M = '||'
message = str(S) + M + str(A)
# need to take part of chal, or the result will be influenced by the limit of Number in python
chal = generate_hash(message)[:10]
cn_value = int.from_bytes(cn, "big") % prime_alea
chal_value = int.from_bytes(chal, "big") % prime_alea

# cn_value = 5
# chal_value = 9
print("cn = ", cn_value)
print("chal = ", chal_value)


resp = w - cn_value * chal_value % prime_alea
# to test if chal = hash...
Pcn = fastExpMod(g, cn_value, prime_alea)
b1 = fastExpMod(Pcn, chal_value, prime_alea)
b2 = fastExpMod(g, resp, prime_alea)
B = b1 * b2 % prime_alea

print(B)
print(B == A)
print(fastExpMod(g, (resp + chal_value * cn_value % prime_alea), prime_alea) == A)
"""
print(myPow(2, 50, prime_alea) * myPow(2, 50, prime_alea) == myPow(2, 100, prime_alea))  # False
# 艹，pow_mod 是错的
print(fastExpMod(2, 50, prime_alea) * fastExpMod(2, 50, prime_alea) == fastExpMod(2, 100, prime_alea))   # True
"""
