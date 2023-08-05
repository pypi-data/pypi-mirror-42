# cython: language_level=3

#include 'bip32.pxi'


cdef extern from "nist256p1.h":
    ctypedef unsigned char ed25519_signature[64]
    ctypedef unsigned char ed25519_public_key[32]
    ctypedef unsigned char ed25519_secret_key[32]

    ctypedef unsigned char curve25519_key[32]

    ctypedef unsigned char ed25519_cosi_signature[32]

    void ed25519_publickey(ed25519_secret_key sk, ed25519_public_key pk)

    int ed25519_sign_open(unsigned char *m, size_t mlen, ed25519_public_key pk, ed25519_signature RS)
    void ed25519_sign(unsigned char *m, size_t mlen, ed25519_secret_key sk, ed25519_public_key pk, ed25519_signature RS)

    int ed25519_scalarmult(ed25519_public_key res, ed25519_secret_key sk, ed25519_public_key pk)

    void curve25519_scalarmult(curve25519_key mypublic, curve25519_key secret, curve25519_key basepoint)
    void curve25519_scalarmult_basepoint(curve25519_key mypublic, curve25519_key secret)

    int ed25519_cosi_combine_publickeys(ed25519_public_key res, ed25519_public_key *pks, size_t n)
    void ed25519_cosi_combine_signatures(ed25519_signature res, ed25519_public_key R, ed25519_cosi_signature *sigs, size_t n)
    void ed25519_cosi_sign(unsigned char *m, size_t mlen, ed25519_secret_key key, ed25519_secret_key nonce, ed25519_public_key R, ed25519_public_key pk, ed25519_cosi_signature sig)
