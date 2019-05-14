# Challenge: KPN CISO Labs, May 7, 2019, Version 1.0.0
import math
from time import time

def gf_inv():
    pass


def bs_gs(p, g, h):
    """ Baby-step Giant-step algorithm """
    m = math.ceil(math.sqrt(p))
    m_negative = gf_inv(pow(g, m))

    m_dict = {}
    for y in range(m):
        m_dict[pow(g, y, p)] = y
        # if y % (m * 0.1) == 0:
        #     print("%.2f %s" % ((y/m)*100, '%'))

    yikes, q = 0, -1
    while not m_dict.get(yikes, False):
        q += 1
        yikes = h * pow(m_negative, q, p) % p

    return m * q + m_dict[yikes]


def brute_force(p, gen, target):
    """ Brute force RSA """
    x, product = 1, gen
    while product != target:
        x += 1
        product = (product * gen) % p
    return x


def time_func(func, msg='', *args, **kwargs):
    """ Function to time specified function """
    start = time()
    output = func(*args, **kwargs)
    print(f"{msg}: {time() - start}")
    return output


# RSA data to crack
# format: bits, prime, gen, target
rsa_data = ((5, 31, 3, 6),
            (13, 7919, 7, 854),
            (20, 688889, 13, 490760),
            (36, 51539607551, 19, 43511947506))

# run tests
for rsa in rsa_data:
    print(time_func(bs_gs, f"BS GS {rsa[0]} bits", *rsa[1:]))
    print(time_func(brute_force, f"Brute force {rsa[0]} bits", *rsa[1:]), end="\n\n")

"""
BS GS 5 bits: 0.0
Brute force 5 bits: 0.0
Key: 25

BS GS 13 bits: 0.000998
Brute force 13 bits: 0.0
Key: 234

BS GS 20 bits: 0.003
Brute force 20 bits: 0.095
Key: 676545

BS GS 36 bits: 1.22
Brute force 36 bits: 129.91
Key: 584050353

Key for 57 bits: 947234702
"""
