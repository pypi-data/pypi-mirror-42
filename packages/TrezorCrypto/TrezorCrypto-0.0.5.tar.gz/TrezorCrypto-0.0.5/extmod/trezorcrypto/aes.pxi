# cython: language_level=3

from libc.stdint cimport uint32_t, uint8_t

cdef extern from "aes.h":

    DEF AES_256 = 1
    DEF AES_MODES = 1
    DEF AES_ENCRYPT = 1
    DEF AES_DECRYPT = 1
    DEF AES_BLOCK_SIZE_P2 = 4
    DEF AES_BLOCK_SIZE = 1 << AES_BLOCK_SIZE_P2
    DEF N_COLS = 4
    DEF KS_LENGTH = 60

    ctypedef union aes_inf:
        uint32_t l
        uint8_t b[4]

    ctypedef struct aes_encrypt_ctx:
        uint32_t ks[KS_LENGTH]
        aes_inf inf

    ctypedef struct aes_decrypt_ctx:
        uint32_t ks[KS_LENGTH]
        aes_inf inf

    int aes_init()
    int aes_encrypt_key256(const unsigned char *key, aes_encrypt_ctx cx[1])
    int aes_decrypt_key256(const unsigned char *key, aes_decrypt_ctx cx[1])

    int aes_ecb_encrypt(const unsigned char *ibuf, unsigned char *obuf, int len, const aes_encrypt_ctx cx[1])
    int aes_ecb_decrypt(const unsigned char *ibuf, unsigned char *obuf, int len, const aes_decrypt_ctx cx[1])
    int aes_cbc_encrypt(const unsigned char *ibuf, unsigned char *obuf, int len, unsigned char *iv, const aes_encrypt_ctx cx[1])
    int aes_cbc_decrypt(const unsigned char *ibuf, unsigned char *obuf, int len, unsigned char *iv, const aes_decrypt_ctx cx[1])

    int aes_cfb_encrypt(const unsigned char *ibuf, unsigned char *obuf, int len, unsigned char *iv, aes_encrypt_ctx cx[1])
    int aes_cfb_decrypt(const unsigned char *ibuf, unsigned char *obuf, int len, unsigned char *iv, aes_encrypt_ctx cx[1])

    int aes_ofb_crypt(const unsigned char *ibuf, unsigned char *obuf, int len, unsigned char *iv, aes_encrypt_ctx cx[1])
    int aes_ofb_encrypt(const unsigned char *ibuf, unsigned char *obuf, int len, unsigned char *iv, aes_encrypt_ctx cx[1])
    int aes_ofb_decrypt(const unsigned char *ibuf, unsigned char *obuf, int len, unsigned char *iv, aes_encrypt_ctx cx[1])

    ctypedef void cbuf_inc(unsigned char *cbuf)

    int aes_ctr_crypt(const unsigned char *ibuf, unsigned char *obuf, int len, unsigned char *cbuf, cbuf_inc ctr_inc, aes_encrypt_ctx cx[1])
    void aes_ctr_cbuf_inc(unsigned char *cbuf)
