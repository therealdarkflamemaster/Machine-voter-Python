from Chiffrrement.pythonSHA256 import generate_hash


# this function is used to realize the HMAC-SHA256

def hashed_mac(key, data, hash_func=generate_hash):
    if not isinstance(key, bytes):
        raise TypeError('key must be bytes')
    if not isinstance(data, bytes):
        raise TypeError('data must be bytes')

    if len(key) > 64:
        key = hash_func(key)

    key += b'\x00' * (64 - len(key))

    v = bytearray(64)
    array_key = bytearray(key)

    for idx, i in enumerate(array_key):
        v[idx] = i ^ 0x36
    ipad = bytes(v)

    for idx, i in enumerate(array_key):
        v[idx] = i ^ 0x5c
    opad = bytes(v)

    return hash_func(opad + hash_func(ipad + data))


# # 0e2564b7e100f034341ea477c23f283b
# print(bytearray(hashed_mac(b'hello', b'world', generate_hash)).hex())
