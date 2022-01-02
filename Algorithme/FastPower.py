# this function is used to calculate quickly the power with deux numbers

def pow_mod(base, pow, mod):
    result = 1
    while pow > 0:
        if pow & 1 == 0:
            result = result * base % mod
        base = base * base % mod
        pow = pow >> 1
    return result


def fastExp(b, e):
    result = 1
    while e != 0:
        if (e & 1) == 1:
            result = (result * b)
        e >>= 1
        b = b * b
    return result


def fastExpMod(b, e, m):
    result = 1
    while e > 0:
        if (e & 1) == 1:
            # ei = 1, then mul
            result = (result * b) % m
        e >>= 1
        # b, b^2, b^4, b^8, ... , b^(2^n)
        b = (b * b) % m
    return result

