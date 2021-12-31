import math


class SHA256:

    def __init__(self):
        self.h = (
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        )
        self.constants = (
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
            0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
            0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
            0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
            0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
            0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
            0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        )

    def padding(self, W):
        return bytes(W, "ascii") + b"\x80" + (b"\x00" * ((55 if (len(W) % 64) < 56 else 119) - (len(W) % 64))) + (
            (len(W) << 3).to_bytes(8, "big"))

    def ch(self,x,y,z):
        c =(x&y)^(~x&z)
        return c

    def ma(self,x,y,z):
        m =(x&y)^(x^z)^(y^z)
        return m

    def right(self,s,n):
        return (s >> n) | (s << (32 - n))

    def itera(self, a, b, c, d, e, f, g, h, w, k):
        x= (d + h + self.ch(e, f, g) + (w + k) + ( self.right(e,6) + self.right(e,11) + self.right(e,25))) % (math.pow(2,32))
        y= (h + self.ch(e,f,g) + ( self.right(e,6) + self.right(e,11) + self.right(e,25)) + self.ma(a,b,c) + (self.right(a,2)+self.right(a,13)+self.right(a,22))) % (math.pow(2,32))
        return y, a, b, c, x, e, f, g

    def Hash(self, message):
        message = self.padding(message)
        digest = list(self.h)

        for i in range(0, len(message), 64):
            S = message[i: i + 64]
            W = [int.from_bytes(S[e: e + 4], "big") for e in range(0, 64, 4)] + ([0] * 48)

            # 构造64个word
            for j in range(16, 64):
                W[j] = (W[j - 16] + (
                        self.right(W[j - 15], 7) ^ self.right(W[j - 15], 18) ^ (W[j - 15] >> 3)) + W[
                            j - 7] + (self.right(W[j - 2], 17) ^ self.right(W[j - 2], 19) ^ (
                        W[j - 2] >> 10))) & ((2 ** 32) - 1)

            a,b,c,d,e,f,g,h = digest

            for j in range(64):
                a,b,c,d,e,f,g,h = self.itera(W[j], self.constants[j], a,b,c,d,e,f,g,h)

        return "".join(format(h, "02x") for h in b"".join(
            d.to_bytes(4, "big") for d in
            [(x + y) & ((2 ** 32) - 1) for x, y in zip(digest, (a,b,c,d,e,f,g,h))]))


# test case
if __name__ == "__main__":
    sha256 = SHA256()
    print(sha256.Hash(bin(11)))
