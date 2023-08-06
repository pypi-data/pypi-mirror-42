# cython: language_level=3

from libc.stdint cimport uint8_t, uint32_t, uint64_t


cdef extern from "sha2.h":

    DEF SHA1_BLOCK_LENGTH = 64
    DEF SHA1_DIGEST_LENGTH = 20
    DEF SHA1_DIGEST_STRING_LENGTH = SHA1_DIGEST_LENGTH * 2 + 1
    DEF SHA256_BLOCK_LENGTH = 64
    DEF SHA256_DIGEST_LENGTH = 32
    DEF SHA256_DIGEST_STRING_LENGTH = SHA256_DIGEST_LENGTH * 2 + 1
    DEF SHA512_BLOCK_LENGTH = 128
    DEF SHA512_DIGEST_LENGTH = 64
    DEF SHA512_DIGEST_STRING_LENGTH = SHA512_DIGEST_LENGTH * 2 + 1

    DEF LITTLE_ENDIAN = 1234
    DEF BIG_ENDIAN = 4321

    ctypedef struct SHA1_CTX:
        uint32_t    state[5]
        uint64_t    bitcount
        uint32_t    buffer[SHA1_BLOCK_LENGTH//4]
    ctypedef struct SHA256_CTX:
        uint32_t    state[8]
        uint64_t    bitcount
        uint32_t    buffer[SHA256_BLOCK_LENGTH//4]
    ctypedef struct SHA512_CTX:
        uint64_t    state[8]
        uint64_t    bitcount[2]
        uint64_t    buffer[SHA512_BLOCK_LENGTH//8]

    extern const uint32_t sha256_initial_hash_value[8]
    extern const uint64_t sha512_initial_hash_value[8]

    void sha1_Transform(const uint32_t* state_in, const uint32_t* data, uint32_t* state_out)
    void sha1_Init(SHA1_CTX *)
    void sha1_Update(SHA1_CTX*, const uint8_t*, size_t)
    void sha1_Final(SHA1_CTX*, uint8_t[SHA1_DIGEST_LENGTH])
    char* sha1_End(SHA1_CTX*, char[SHA1_DIGEST_STRING_LENGTH])
    void sha1_Raw(const uint8_t*, size_t, uint8_t[SHA1_DIGEST_LENGTH])
    char* sha1_Data(const uint8_t*, size_t, char[SHA1_DIGEST_STRING_LENGTH])

    void sha256_Transform(const uint32_t* state_in, const uint32_t* data, uint32_t* state_out)
    void sha256_Init(SHA256_CTX *)
    void sha256_Update(SHA256_CTX*, const uint8_t*, size_t)
    void sha256_Final(SHA256_CTX*, uint8_t[SHA256_DIGEST_LENGTH])
    char* sha256_End(SHA256_CTX*, char[SHA256_DIGEST_STRING_LENGTH])
    void sha256_Raw(const uint8_t*, size_t, uint8_t[SHA256_DIGEST_LENGTH])
    char* sha256_Data(const uint8_t*, size_t, char[SHA256_DIGEST_STRING_LENGTH])

    void sha512_Transform(const uint64_t* state_in, const uint64_t* data, uint64_t* state_out)
    void sha512_Init(SHA512_CTX*)
    void sha512_Update(SHA512_CTX*, const uint8_t*, size_t)
    void sha512_Final(SHA512_CTX*, uint8_t[SHA512_DIGEST_LENGTH])
    char* sha512_End(SHA512_CTX*, char[SHA512_DIGEST_STRING_LENGTH])
    void sha512_Raw(const uint8_t*, size_t, uint8_t[SHA512_DIGEST_LENGTH])
    char* sha512_Data(const uint8_t*, size_t, char[SHA512_DIGEST_STRING_LENGTH])
