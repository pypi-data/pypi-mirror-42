# cython: language_level=3

include 'ecdsa.pxi'

from libc.stdint cimport uint32_t, uint8_t


cdef extern from "bip32.h":
    ctypedef struct curve_info:
        const char *bip32_name
        const ecdsa_curve *params
        HasherType hasher_base58
        HasherType hasher_sign
        HasherType hasher_pubkey
        HasherType hasher_script

    ctypedef struct HDNode:
        uint32_t depth
        uint32_t child_num
        uint8_t chain_code[32]
        uint8_t private_key[32]
        uint8_t private_key_extension[32]
        uint8_t public_key[33]
        const curve_info *curve

    int hdnode_from_xpub(uint32_t depth, uint32_t child_num, const uint8_t *chain_code, const uint8_t *public_key, const char *curve, HDNode *out)

    int hdnode_from_xprv(uint32_t depth, uint32_t child_num, const uint8_t *chain_code, const uint8_t *private_key, const char *curve, HDNode *out)

    int hdnode_from_seed(const uint8_t *seed, int seed_len, const char *curve, HDNode *out)

    int hdnode_private_ckd(HDNode *inout, uint32_t i)

    int hdnode_private_ckd_prime(HDNode *inout, uint32_t i)

    int hdnode_public_ckd_cp(const ecdsa_curve *curve, const curve_point *parent, const uint8_t *parent_chain_code, uint32_t i, curve_point *child, uint8_t *child_chain_code)

    int hdnode_public_ckd(HDNode *inout, uint32_t i)

    void hdnode_public_ckd_address_optimized(const curve_point *pub, const uint8_t *chain_code, uint32_t i, uint32_t version, HasherType hasher_pubkey, HasherType hasher_base58, char *addr, int addrsize, int addrformat)

    int hdnode_private_ckd_cached(HDNode *inout, const uint32_t *i, size_t i_count, uint32_t *fingerprint)

    uint32_t hdnode_fingerprint(HDNode *node)

    void hdnode_fill_public_key(HDNode *node)

    int hdnode_sign(HDNode *node, const uint8_t *msg, uint32_t msg_len, HasherType hasher_sign, uint8_t *sig, uint8_t *pby, int (*is_canonical)(uint8_t by, uint8_t sig[64]))
    int hdnode_sign_digest(HDNode *node, const uint8_t *digest, uint8_t *sig, uint8_t *pby, int (*is_canonical)(uint8_t by, uint8_t sig[64]))

    int hdnode_get_shared_key(const HDNode *node, const uint8_t *peer_public_key, uint8_t *session_key, int *result_size)

    int hdnode_serialize_public(const HDNode *node, uint32_t fingerprint, uint32_t version, char *str, int strsize)

    int hdnode_serialize_private(const HDNode *node, uint32_t fingerprint, uint32_t version, char *str, int strsize)

    int hdnode_deserialize(const char *str, uint32_t version_public, uint32_t version_private, const char *curve, HDNode *node, uint32_t *fingerprint)

    void hdnode_get_address_raw(HDNode *node, uint32_t version, uint8_t *addr_raw)
    void hdnode_get_address(HDNode *node, uint32_t version, char *addr, int addrsize)

    const curve_info *get_curve_by_name(const char *curve_name)
