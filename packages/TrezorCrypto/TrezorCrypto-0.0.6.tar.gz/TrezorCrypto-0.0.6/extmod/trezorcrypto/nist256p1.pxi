# cython: language_level=3

include 'bip32.pxi'


cdef extern from "nist256p1.h":
    extern const ecdsa_curve nist256p1
    extern const curve_info nist256p1_info
