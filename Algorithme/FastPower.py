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


def myPow(x: float, n: int, m: int) -> float:
    def quickMul(N):
        ans = 1.0
        # 贡献的初始值为 x
        x_contribute = x
        # 在对 N 进行二进制拆分的同时计算答案
        while N > 0:
            if N % 2 == 1:
                # 如果 N 二进制表示的最低位为 1，那么需要计入贡献
                ans = ans * x_contribute % m
            # 将贡献不断地平方
            x_contribute = x_contribute * x_contribute % m
            # 舍弃 N 二进制表示的最低位，这样我们每次只要判断最低位即可
            N //= 2
        return ans

    return quickMul(n) if n >= 0 else 1.0 / quickMul(-n)
