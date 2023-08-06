# cython: language_level=3

include 'options.pxi'


cdef extern from 'hasher.h':
    IF USE_KECCAK:
        ctypedef enum HasherType:
            HASHER_SHA2
            HASHER_SHA2D
            HASHER_SHA2_RIPEMD
            HASHER_SHA3
            HASHER_SHA3K
            HASHER_BLAKE
            HASHER_BLAKED
            HASHER_BLAKE_RIPEMD
            HASHER_GROESTLD_TRUNC
            HASHER_OVERWINTER_PREVOUTS
            HASHER_OVERWINTER_SEQUENCE
            HASHER_OVERWINTER_OUTPUTS
            HASHER_OVERWINTER_PREIMAGE
            HASHER_SAPLING_PREIMAGE
    ELSE:
        ctypedef enum HasherType:
            HASHER_SHA2
            HASHER_SHA2D
            HASHER_SHA2_RIPEMD
            HASHER_SHA3
            HASHER_BLAKE
            HASHER_BLAKED
            HASHER_BLAKE_RIPEMD
            HASHER_GROESTLD_TRUNC
            HASHER_OVERWINTER_PREVOUTS
            HASHER_OVERWINTER_SEQUENCE
            HASHER_OVERWINTER_OUTPUTS
            HASHER_OVERWINTER_PREIMAGE
            HASHER_SAPLING_PREIMAGE
