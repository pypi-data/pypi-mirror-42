# cython: language_level=3

include 'bignum.pxi'

from libc.stdint cimport uint32_t, uint8_t, uint64_t

cdef extern from "rfc6979.h":
    ctypedef struct rfc6979_state:
        uint8_t v[32]
        uint8_t k[32]

    void init_rfc6979(const uint8_t *priv_key, const uint8_t *hash, rfc6979_state *rng)
    void generate_rfc6979(uint8_t rnd[32], rfc6979_state *rng)
    void generate_k_rfc6979(bignum256 *k, rfc6979_state *rng)
