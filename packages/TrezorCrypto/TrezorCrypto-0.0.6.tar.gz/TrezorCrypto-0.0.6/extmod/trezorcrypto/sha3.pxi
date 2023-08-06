# cython: language_level=3

from libc.stdint cimport uint64_t


cdef extern from "sha3.h":
    DEF sha3_256_hash_size = 32
    DEF sha3_512_hash_size = 64
    DEF sha3_max_permutation_size = 25
    DEF sha3_max_rate_in_qwords = 24

    DEF SHA3_256_BLOCK_LENGTH = 136
    DEF SHA3_512_BLOCK_LENGTH = 72

    DEF SHA3_256_DIGEST_LENGTH = sha3_256_hash_size
    DEF SHA3_512_DIGEST_LENGTH = sha3_512_hash_size

    ctypedef struct SHA3_CTX:
        # 1600 bits algorithm hashing state
        uint64_t hash[sha3_max_permutation_size]
        # 1536-bit buffer for leftovers
        uint64_t message[sha3_max_rate_in_qwords]
        # count of bytes in the message[] buffer
        unsigned rest
        # size of a message block processed at once
        unsigned block_size

    void sha3_256_Init(SHA3_CTX *ctx);
    void sha3_512_Init(SHA3_CTX *ctx);
    void sha3_Update(SHA3_CTX *ctx, const unsigned char* msg, size_t size);
    void sha3_Final(SHA3_CTX *ctx, unsigned char* result);
    void keccak_Final(SHA3_CTX *ctx, unsigned char* result);
