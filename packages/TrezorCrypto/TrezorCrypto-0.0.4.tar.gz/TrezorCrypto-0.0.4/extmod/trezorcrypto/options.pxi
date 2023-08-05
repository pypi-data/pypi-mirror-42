# cython: language_level=3

cdef extern from 'options.h':
    # use precomputed Curve Points (some scalar multiples of curve base point G)
    DEF USE_PRECOMPUTED_CP = 1

    # use fast inverse method
    DEF USE_INVERSE_FAST = 1

    # support for printing bignum256 structures via printf
    DEF USE_BN_PRINT = 0

    # use deterministic signatures
    DEF USE_RFC6979 = 1

    # implement BIP32 caching
    DEF USE_BIP32_CACHE = 1
    DEF BIP32_CACHE_SIZE = 10
    DEF BIP32_CACHE_MAXDEPTH = 8

    # support constructing BIP32 nodes from ed25519 and curve25519 curves.
    DEF USE_BIP32_25519_CURVES = 1

    # implement BIP39 caching
    DEF USE_BIP39_CACHE = 1
    DEF BIP39_CACHE_SIZE = 4

    # support Ethereum operations
    DEF USE_ETHEREUM = 0

    # support Graphene operations (STEEM, BitShares)
    DEF USE_GRAPHENE = 0

    # support NEM operations
    DEF USE_NEM = 0

    # support MONERO operations
    DEF USE_MONERO = 0

    # support CARDANO operations
    DEF USE_CARDANO = 0

    # support Keccak hashing
    DEF USE_KECCAK = 1

    # add way how to mark confidential data
    DEF CONFIDENTIAL = 1
