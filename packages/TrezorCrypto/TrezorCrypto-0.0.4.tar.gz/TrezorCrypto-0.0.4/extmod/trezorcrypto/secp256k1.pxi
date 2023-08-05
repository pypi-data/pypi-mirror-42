# cython: language_level=3

include 'bip32.pxi'


cdef extern from "secp256k1.h":
    extern const ecdsa_curve secp256k1
    extern const curve_info secp256k1_info
