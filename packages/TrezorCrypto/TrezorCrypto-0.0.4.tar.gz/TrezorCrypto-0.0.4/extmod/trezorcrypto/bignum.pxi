# cython: language_level=3

from libc.stdint cimport uint32_t


cdef extern from 'bignum.h':
    ctypedef struct bignum256:
        uint32_t val[9]
