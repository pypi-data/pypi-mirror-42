
cdef extern from "curves.h":
    extern const char SECP256K1_NAME[]
    extern const char SECP256K1_DECRED_NAME[]
    extern const char SECP256K1_GROESTL_NAME[]
    extern const char SECP256K1_SMART_NAME[]
    extern const char NIST256P1_NAME[]
    extern const char ED25519_NAME[]
    extern const char ED25519_CARDANO_NAME[]
    extern const char ED25519_SHA3_NAME[]
    extern const char ED25519_KECCAK_NAME[]
    extern const char CURVE25519_NAME[]
