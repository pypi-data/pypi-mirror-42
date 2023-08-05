# cython: language_level=3

# hashlib implementation
include 'sha2.pxi'
include 'sha3.pxi'
include 'ripemd160.pxi'

from libc.stdint cimport uint8_t, uint32_t
from libc.string cimport memcpy
from cpython cimport PyBytes_FromStringAndSize, PyUnicode_InternFromString

cimport sha2
cimport sha3
cimport ripemd160 as ripemd


cdef class sha1:
    cdef SHA1_CTX ctx

    def __init__(self, data=None):
        sha2.sha1_Init(&self.ctx)
        if data is None:
            return
        self.update(data)

    def update(self, data):
        data_len = len(data)
        if data_len > 0:
            sha2.sha1_Update(&self.ctx, data, data_len)

    def digest(self):
        cdef uint8_t out[SHA1_DIGEST_LENGTH]
        cdef SHA1_CTX ctx
        memcpy(&ctx, &self.ctx, sizeof(SHA1_CTX))
        sha2.sha1_Final(&ctx, out)
        return PyBytes_FromStringAndSize(<char *>out, SHA1_DIGEST_LENGTH)

    @property
    def digest_size(self):
        return SHA1_DIGEST_LENGTH

    @property
    def block_size(self):
        return SHA1_BLOCK_LENGTH


cdef class sha256:
    cdef SHA256_CTX ctx

    def __init__(self, data=None):
        sha2.sha256_Init(&self.ctx)
        if data is None:
            return
        self.update(data)

    def update(self, data):
        data_len = len(data)
        if data_len > 0:
            sha2.sha256_Update(&self.ctx, data, data_len)

    def digest(self):
        cdef uint8_t out[SHA256_DIGEST_LENGTH]
        cdef SHA256_CTX ctx
        memcpy(&ctx, &self.ctx, sizeof(SHA256_CTX))
        sha2.sha256_Final(&ctx, out)
        return PyBytes_FromStringAndSize(<char *>out, SHA256_DIGEST_LENGTH)

    @property
    def digest_size(self):
        return SHA256_DIGEST_LENGTH

    @property
    def block_size(self):
        return SHA256_BLOCK_LENGTH


cdef class sha512:
    cdef SHA512_CTX ctx

    def __init__(self, data=None):
        sha2.sha512_Init(&self.ctx)
        if data is None:
            return
        self.update(data)

    def update(self, data):
        data_len = len(data)
        if data_len > 0:
            sha2.sha512_Update(&self.ctx, data, data_len)

    def digest(self):
        cdef uint8_t out[SHA512_DIGEST_LENGTH]
        cdef SHA512_CTX ctx
        memcpy(&ctx, &self.ctx, sizeof(SHA512_CTX))
        sha2.sha512_Final(&ctx, out)
        return PyBytes_FromStringAndSize(<char *>out, SHA512_DIGEST_LENGTH)

    @property
    def digest_size(self):
        return SHA512_DIGEST_LENGTH

    @property
    def block_size(self):
        return SHA512_BLOCK_LENGTH


cdef class sha3_256:
    cdef SHA3_CTX ctx

    def __init__(self, data=None, keccak=False):
        self.keccak = keccak
        sha3.sha3_256_Init(&self.ctx)
        if data is None:
            return
        self.update(data)

    def update(self, data):
        data_len = len(data)
        if data_len > 0:
            sha3.sha3_Update(&self.ctx, data, data_len)

    def digest(self):
        cdef uint8_t out[SHA3_256_DIGEST_LENGTH]
        cdef SHA3_CTX ctx
        memcpy(&ctx, &self.ctx, sizeof(SHA3_CTX))
        if self.keccak:
            sha3.keccak_Final(&ctx, out)
        else:
            sha3.sha3_Final(&ctx, out)
        return PyBytes_FromStringAndSize(<char *>out, SHA3_256_DIGEST_LENGTH)

    @property
    def digest_size(self):
        return SHA3_256_DIGEST_LENGTH

    @property
    def block_size(self):
        return SHA3_256_BLOCK_LENGTH


cdef class sha3_512:
    cdef SHA3_CTX ctx

    def __init__(self, data=None, keccak=False):
        self.keccak = keccak
        sha3.sha3_512_Init(&self.ctx)
        if data is None:
            return
        self.update(data)

    def update(self, data):
        data_len = len(data)
        if data_len > 0:
            sha3.sha3_Update(&self.ctx, data, data_len)

    def digest(self):
        cdef uint8_t out[SHA3_512_DIGEST_LENGTH]
        cdef SHA3_CTX ctx
        memcpy(&ctx, &self.ctx, sizeof(SHA3_CTX))
        if self.keccak:
            sha3.keccak_Final(&ctx, out)
        else:
            sha3.sha3_Final(&ctx, out)
        return PyBytes_FromStringAndSize(<char *>out, SHA3_512_DIGEST_LENGTH)

    @property
    def digest_size(self):
        return SHA3_512_DIGEST_LENGTH

    @property
    def block_size(self):
        return SHA3_512_BLOCK_LENGTH


cdef class ripemd160:
    cdef RIPEMD160_CTX ctx

    def __init__(self, data=None):
        ripemd.ripemd160_Init(&self.ctx)
        if data is None:
            return
        self.update(data)

    def update(self, data):
        data_len = len(data)
        if data_len > 0:
            ripemd.ripemd160_Update(&self.ctx, data, data_len)

    def digest(self):
        cdef uint8_t out[RIPEMD160_DIGEST_LENGTH]
        cdef RIPEMD160_CTX ctx
        memcpy(&ctx, &self.ctx, sizeof(RIPEMD160_CTX))
        ripemd.ripemd160_Final(&ctx, out)
        return PyBytes_FromStringAndSize(<char *>out, RIPEMD160_DIGEST_LENGTH)

    @property
    def digest_size(self):
        return RIPEMD160_DIGEST_LENGTH

    @property
    def block_size(self):
        return RIPEMD160_BLOCK_LENGTH

# AES implementation
include 'aes.pxi'

cimport aes as caes

ctypedef struct AES_t:
    aes_encrypt_ctx encrypt_ctx
    aes_decrypt_ctx decrypt_ctx
    int mode
    uint8_t iv[AES_BLOCK_SIZE]


cdef class aes:
    '''
    AES context.
    '''
    ECB = 0x00
    CBC = 0x01
    CFB = 0x02
    OFB = 0x03
    CTR = 0x04
    cdef AES_t cAES

    def __init__(self, mode, key, iv=None):
        '''
        Initialize AES context.
        '''
        self.cAES.mode = mode
        if mode < self.ECB or  mode > self.CTR:
            raise ValueError('Invalid AES mode')
        key_len = len(key)
        if key_len != 32:
            raise ValueError('Invalid length of key (has to be 256 bits)')
        if iv is None:
            self.cAES.iv = <uint8_t *>(b'\x00'*AES_BLOCK_SIZE)
        else:
            iv_len = len(iv)
            if iv_len != AES_BLOCK_SIZE:
                raise ValueError('Invalid length of initialization '
                                 'vector (has to be 128 bits)')
            self.cAES.iv = <uint8_t *>iv

        if key_len == 32:
            caes.aes_decrypt_key256(key, &self.cAES.decrypt_ctx)
            caes.aes_encrypt_key256(key, &self.cAES.encrypt_ctx)

    def update(self, data, encrypt):
        '''
        Update AES context with data.
        '''
        data_len = len(data)
        odata = bytearray(data)
        if data_len == 0:
            return b''
        mode = self.cAES.mode
        if mode == self.ECB:
            if data_len & (AES_BLOCK_SIZE - 1):
                raise ValueError('Invalid data length')
            if encrypt:
                caes.aes_ecb_encrypt(<uint8_t *>data, <uint8_t *>odata,
                                     data_len, &self.cAES.encrypt_ctx)
            else:
                caes.aes_ecb_decrypt(<uint8_t *>data, <uint8_t *>odata,
                                     data_len, &self.cAES.decrypt_ctx)
        elif mode == self.CBC:
            if data_len & (AES_BLOCK_SIZE - 1):
                raise ValueError('Invalid data length')
            if encrypt:
                caes.aes_cbc_encrypt(<uint8_t *>data, <uint8_t *>odata,
                                     data_len, self.cAES.iv,
                                     &self.cAES.encrypt_ctx)
            else:
                caes.aes_cbc_decrypt(<uint8_t *>data, <uint8_t *>odata,
                                     data_len, self.cAES.iv,
                                     &self.cAES.decrypt_ctx)
        elif mode == self.CFB:
            if encrypt:
                caes.aes_cfb_encrypt(<uint8_t *>data, <uint8_t *>odata,
                                     data_len, self.cAES.iv,
                                     &self.cAES.encrypt_ctx)
            else:
                caes.aes_cfb_decrypt(<uint8_t *>data, <uint8_t *>odata,
                                     data_len, self.cAES.iv,
                                     &self.cAES.encrypt_ctx)
        elif mode == self.OFB:
            caes.aes_ofb_crypt(<uint8_t *>data, <uint8_t *>odata,
                               data_len, self.cAES.iv, &self.cAES.encrypt_ctx)
        elif mode == self.CTR:
            caes.aes_ctr_crypt(<uint8_t *>data, <uint8_t *>odata,
                               data_len, self.cAES.iv, caes.aes_ctr_cbuf_inc,
                               &self.cAES.encrypt_ctx)

        return PyBytes_FromStringAndSize(<char *>odata, data_len)

    def encrypt(self, data):
        '''
        Encrypt data and update AES context.
        '''
        return self.update(data, True)

    def decrypt(self, data):
        '''
        Decrypt data and update AES context.
        '''
        return self.update(data, False)


# bip32 implementation
include 'curves.pxi'

cimport bip32 as cbip32

import binascii


hfu = binascii.hexlify


DEF XPUB_MAXLEN = 128
DEF ADDRESS_MAXLEN = 36


cdef class HDNodeBase:
    '''
    BIP0032 HD node structure.
    '''
    cdef const cbip32.curve_info *_curve_info
    cdef cbip32.HDNode _HDNode
    cdef uint32_t _HDNode_fingerprint

    def __str__(self):
        private_key = self.private_key()
        private_key = hfu(private_key) if private_key else private_key
        public_key = self.public_key()
        public_key = hfu(public_key) if public_key else public_key
        return ('HDNodeBase\n\tdepth: {}\n\tfingerprint: {}\n\t'
                'child_num: {}\n\tchain_code: {}\n\tpriv: {}\n\t'
                'pub: {}\n'.format(
                self.depth(),
                self.fingerprint(),
                self.child_num(),
                hfu(self.chain_code()),
                private_key,
                public_key
        ))

    def __init__(self,
                 depth: int,
                 fingerprint: int,
                 child_num: int,
                 chain_code,
                 private_key=None,
                 public_key=None,
                 curve_name=None):
        if private_key is None:
           private_key = b'\x00'*32
        if public_key is None:
           public_key = b'\x00'*33

        if len(chain_code) != 32:
            raise ValueError('chain_code is invalid')
        if len(private_key) != 0 and len(private_key) != 32:
            raise ValueError('private_key is invalid')
        if len(public_key) != 0 and len(public_key) != 33:
            raise ValueError('public_key is invalid')
        if len(public_key) == 0 and len(private_key) == 0:
            raise ValueError('either public_key or private_key is required')

        if curve_name:
            self._curve_info = cbip32.get_curve_by_name(curve_name)
        else:
            self._curve_info = cbip32.get_curve_by_name(SECP256K1_NAME)
        if self._curve_info == NULL:
            raise ValueError('curve_name is invalid')

        self._HDNode_fingerprint = fingerprint
        self._HDNode.depth = depth
        self._HDNode.child_num = child_num
        self._HDNode.chain_code = <uint8_t *> chain_code
        self._HDNode.private_key = <uint8_t *> private_key
        self._HDNode.public_key = <uint8_t *> public_key
        self._HDNode.curve = self._curve_info

    def derive(self, index: int, public: bool=False) -> None:
        '''
        Derive a BIP0032 child node in place.
        '''
        cdef uint32_t fp = cbip32.hdnode_fingerprint(&self._HDNode)
        if public:
            res = cbip32.hdnode_public_ckd(&self._HDNode, index)
        else:
            zeropk = b'\x00'*32
            private_key = PyBytes_FromStringAndSize(<char *>self._HDNode.private_key, 32)
            if private_key == zeropk:
                raise ValueError('Failed to derive, private key not set')
            res = cbip32.hdnode_private_ckd(&self._HDNode, index)
        if not res:
            raise ValueError('Failed to derive')
        self._HDNode_fingerprint = fp

    def derive_path(self, path) -> None:
        '''
        Go through a list of indexes and iteratively derive a child node in place.
        '''
        cdef int plen = len(path)
        if plen > 32:
            raise ValueError('Path cannot be longer than 32 indexes')
        cdef uint32_t pints[32]
        for i in range(plen):
            pints[i] = path[i]

        if not cbip32.hdnode_private_ckd_cached(&self._HDNode, pints, plen,
                                                &self._HDNode_fingerprint):
            raise ValueError('Failed to derive path')

    def serialize_public(self, version: int) -> str:
        '''
        Serialize the public info from HD node to base58 string.
        '''
        cdef char xpub[XPUB_MAXLEN]
        xpub[0] = 0
        cbip32.hdnode_fill_public_key(&self._HDNode)
        written = cbip32.hdnode_serialize_public(&self._HDNode,
                                                 self._HDNode_fingerprint,
                                                 version, xpub, XPUB_MAXLEN)
        if written <= 0:
            raise ValueError('Failed to serialize')
        bytes_xpub = <bytes> xpub
        return bytes_xpub.decode('utf-8')

    def serialize_private(self, version: int) -> str:
        '''
        Serialize the private info HD node to base58 string.
        '''
        cdef char xpub[XPUB_MAXLEN]
        xpub[0] = 0
        written = cbip32.hdnode_serialize_private(&self._HDNode,
                                                  self._HDNode_fingerprint,
                                                  version, xpub, XPUB_MAXLEN)
        if written <= 0:
            raise ValueError('Failed to serialize')
        bytes_xpub = <bytes> xpub
        return bytes_xpub.decode('utf-8')

    def clone(self) -> HDNodeBase:
        '''
        Returns a copy of the HD node.
        '''
        return HDNodeBase(depth=self.depth(), fingerprint=self.fingerprint(),
                          child_num=self.child_num(),
                          chain_code=self.chain_code(),
                          private_key=self.private_key(),
                          public_key=self.public_key())

    def depth(self) -> int:
        '''
        Returns a depth of the HD node.
        '''
        return self._HDNode.depth

    def fingerprint(self) -> int:
        '''
        Returns a fingerprint of the HD node (hash of the parent public key).
        '''
        return self._HDNode_fingerprint

    def child_num(self) -> int:
        '''
        Returns a child index of the HD node.
        '''
        return self._HDNode.child_num

    def chain_code(self) -> bytes:
        '''
        Returns a chain code of the HD node.
        '''
        return PyBytes_FromStringAndSize(<char *>self._HDNode.chain_code, 32)

    def private_key(self) -> bytes:
        '''
        Returns a private key of the HD node.
        '''
        return PyBytes_FromStringAndSize(<char *>self._HDNode.private_key, 32)

    def public_key(self) -> bytes:
        '''
        Returns a public key of the HD node.
        '''
        cbip32.hdnode_fill_public_key(&self._HDNode)
        return PyBytes_FromStringAndSize(<char *>self._HDNode.public_key, 33)

    def address(self, version: int) -> str:
        '''
        Compute a base58-encoded address string from the HD node.
        '''
        cdef char address[ADDRESS_MAXLEN]
        address[0] = 0
        written = cbip32.hdnode_get_address(&self._HDNode, version,
                                            address, ADDRESS_MAXLEN)
        bytes_address = <bytes> address
        return bytes_address.decode('utf-8')

    def deserialize(self, value: str, version_public: int, version_private: int):
        '''
        Construct a BIP0032 HD node from a base58-serialized value.
        '''
        if len(value) == 0:
            raise ValueError('Invalid value')

        cdef uint32_t vpub = version_public
        cdef uint32_t vpriv = version_private
        cdef cbip32.HDNode hdnode
        cdef uint32_t fingerprint
        if cbip32.hdnode_deserialize(value, vpub, vpriv,
                                    SECP256K1_NAME, &hdnode,
                                    &fingerprint) < 0:
            raise ValueError('Failed to deserialize')
        chain_code = PyBytes_FromStringAndSize(<char *>hdnode.chain_code, 32)
        private_key = PyBytes_FromStringAndSize(<char *>hdnode.private_key, 32)
        public_key = PyBytes_FromStringAndSize(<char *>hdnode.public_key, 33)
        return HDNodeBase(depth=hdnode.depth, fingerprint=fingerprint,
                          child_num=hdnode.child_num,
                          chain_code=chain_code,
                          private_key=private_key,
                          public_key=public_key,
                          curve_name=SECP256K1_NAME)


cpdef inline HDNodeBase from_seed(seed: bytes, curve_name: str):
    '''
    Construct a BIP0032 HD node from a BIP0039 seed value.
    '''
    if len(seed) == 0:
        raise ValueError('Invalid seed')
    if len(curve_name) == 0:
        raise ValueError('Invalid curve name')

    cdef cbip32.HDNode hdnode
    b_curve_name = curve_name.encode('utf-8')
    if not cbip32.hdnode_from_seed(seed, len(seed), b_curve_name, &hdnode):
        raise ValueError('Failed to derive the root node')

    cdef uint32_t fingerprint = 0
    chain_code = PyBytes_FromStringAndSize(<char *>hdnode.chain_code, 32)
    private_key = PyBytes_FromStringAndSize(<char *>hdnode.private_key, 32)
    public_key = PyBytes_FromStringAndSize(<char *>hdnode.public_key, 33)
    return HDNodeBase(depth=hdnode.depth, fingerprint=fingerprint,
                      child_num=hdnode.child_num,
                      chain_code=chain_code,
                      private_key=private_key,
                      public_key=public_key,
                      curve_name=b_curve_name)

class bip32:
    HDNode = HDNodeBase

    @classmethod
    def from_seed(cls, seed: bytes, curve_name: str):
        return from_seed(seed, curve_name)


# bip32 implementation
cimport bip39 as cbip39


def bip39_generate(bits: int) -> str:
    if bits % 32 or bits < 128 or bits > 256:
        raise ValueError('Invalid bit strength (only 128, 160,'
                         ' 192, 224 and 256 values are allowed)')
    cdef const char *mnemo = cbip39.mnemonic_generate(bits)
    return PyUnicode_InternFromString(mnemo)


def bip39_from_data(data: bytes) -> str:
    data_len = len(data)
    if data_len % 4 or data_len < 16 or data_len > 32:
        raise ValueError('Invalid data length (only 16, 20, 24,'
                         ' 28 and 32 bytes are allowed)')
    cdef const char *mnemo = cbip39.mnemonic_from_data(<uint8_t *>data, data_len)
    return PyUnicode_InternFromString(mnemo)


def bip39_check(mnemonic: str) -> bool:
    mnem = mnemonic.encode('utf-8')
    mnem_len = len(mnem)
    return mnem_len > 0 and cbip39.mnemonic_check(<char *>mnem)


def bip39_seed(mnemonic: str, passphrase: str) -> bytes:
    mnem = mnemonic.encode('utf-8')
    pphrase = passphrase.encode('utf-8')
    cdef uint8_t seed[64]
    cbip39.mnemonic_to_seed(<char *>mnem, <char*>pphrase, seed, NULL)
    return PyBytes_FromStringAndSize(<char *>seed, 64)


class bip39:
    generate = bip39_generate
    from_data = bip39_from_data
    check = bip39_check
    seed = bip39_seed


# secp256k1 implementation
include 'rand.pxi'

cimport ecdsa
cimport secp256k1 as csecp256k1


# Wrong secrets
DEF SECP256K1_WS0 = (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00')

DEF SECP256K1_WS1 = (b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
                     b'\xFF\xFF\xFF\xFE\xBA\xAE\xDC\xE6\xAF\x48\xA0\x3B'
                     b'\xBF\xD2\x5E\x8C\xD0\x36\x41\x41')


def secp256k1_generate_secret() -> bytes:
    cdef uint8_t out[32]
    while True:
        random_buffer(out, 32)
        bout = PyBytes_FromStringAndSize(<char *>out, 32)
        if bout != SECP256K1_WS0 and bout != SECP256K1_WS1:
            return bout


def secp256k1_publickey(secret_key, compressed: bool = True) -> bytes:
    if len(secret_key) != 32:
        raise ValueError('Invalid length of secret key')

    cdef uint8_t out33[33]
    cdef uint8_t out65[65]
    if compressed:
        ecdsa.ecdsa_get_public_key33(&csecp256k1.secp256k1,
                                     <const uint8_t *>secret_key, out33)
        return PyBytes_FromStringAndSize(<char *>out33, 33)
    else:
        ecdsa.ecdsa_get_public_key65(&csecp256k1.secp256k1,
                                     <const uint8_t *>secret_key, out65)
        return PyBytes_FromStringAndSize(<char *>out65, 65)


def secp256k1_sign(secret_key, digest, compressed: bool = True) -> bytes:
    if len(secret_key) != 32:
        raise ValueError('Invalid length of secret key')
    if len(digest) != 32:
        raise ValueError('Invalid length of digest')
    cdef uint8_t out[65]
    cdef uint8_t pby
    if 0 != ecdsa.ecdsa_sign_digest(&csecp256k1.secp256k1,
                                    <const uint8_t *>secret_key,
                                    <const uint8_t *>digest,
                                    out + 1, &pby, NULL):
        raise ValueError('Signing failed')
    out[0] = 27 + pby + compressed * 4
    return PyBytes_FromStringAndSize(<char *>out, 65)


def secp256k1_verify(public_key, signature, digest) -> bool:
    pk_len = len(public_key)
    if pk_len != 33 and pk_len != 65:
        raise ValueError('Invalid length of public key')
    sig_len = len(signature)
    if sig_len != 64 and sig_len != 65:
        raise ValueError('Invalid length of signature')
    cdef int offset = sig_len - 64
    dig_len = len(digest)
    if dig_len != 32:
        raise ValueError('Invalid length of digest')
    sig_with_offset = signature[offset:]
    res = ecdsa.ecdsa_verify_digest(&csecp256k1.secp256k1,
                                    <const uint8_t *>public_key,
                                    <const uint8_t *>sig_with_offset,
                                    <const uint8_t *>digest)
    return res == 0


def secp256k1_verify_recover(signature, digest) -> bytes:
    sig_len = len(signature)
    if sig_len != 65:
        raise ValueError('Invalid length of signature')
    dig_len = len(digest)
    if dig_len != 32:
        raise ValueError('Invalid length of digest')
    cdef uint8_t recid = (<const uint8_t>signature[0]) - 27
    if recid >= 8:
        raise ValueError('Invalid recid in signature')
    cdef int compressed = (recid >= 4)
    recid &= 3
    cdef uint8_t out[65]

    sig_with_offset = signature[1:]
    if 0 == ecdsa.ecdsa_recover_pub_from_sig(&csecp256k1.secp256k1, out,
                                             <const uint8_t *>sig_with_offset,
                                             <const uint8_t *>digest, recid):
        if compressed:
            out[0] = 0x02 | (out[64] & 1)
            return PyBytes_FromStringAndSize(<char *>out, 33)
        return PyBytes_FromStringAndSize(<char *>out, 65)
    return None


def secp256k1_multiply(secret_key, public_key) -> bytes:
    sk_len = len(secret_key)
    if sk_len != 32:
        raise ValueError('Invalid length of secret key')
    pk_len = len(public_key)
    if pk_len != 33 and pk_len != 65:
        raise ValueError('Invalid length of public key')
    cdef uint8_t out[65]
    if 0 != ecdsa.ecdh_multiply(&csecp256k1.secp256k1,
                                <const uint8_t *>secret_key,
                                <const uint8_t *>public_key, out):
        raise ValueError('Multiply failed')

    return PyBytes_FromStringAndSize(<char *>out, 65)


class secp256k1:
    generate_secret = secp256k1_generate_secret
    publickey = secp256k1_publickey
    sign = secp256k1_sign
    verify = secp256k1_verify
    verify_recover = secp256k1_verify_recover
    multiply = secp256k1_multiply


# nist256p1 implementation
cimport nist256p1 as cnist256p1


# Wrong secrets
DEF NIST256P1_WS0 = (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00')

DEF NIST256P1_WS1 = (b'\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF'
                     b'\xFF\xFF\xFF\xFF\xBC\xE6\xFA\xAD\xA7\x17\x9E\x84'
                     b'\xF3\xB9\xCA\xC2\xFC\x63\x25\x51')


def nist256p1_generate_secret() -> bytes:
    cdef uint8_t out[32]
    while True:
        random_buffer(out, 32)
        bout = PyBytes_FromStringAndSize(<char *>out, 32)
        if bout != NIST256P1_WS0 and bout != NIST256P1_WS1:
            return bout


def nist256p1_publickey(secret_key, compressed: bool = True) -> bytes:
    if len(secret_key) != 32:
        raise ValueError('Invalid length of secret key')

    cdef uint8_t out33[33]
    cdef uint8_t out65[65]
    if compressed:
        ecdsa.ecdsa_get_public_key33(&cnist256p1.nist256p1,
                                     <const uint8_t *>secret_key, out33)
        return PyBytes_FromStringAndSize(<char *>out33, 33)
    else:
        ecdsa.ecdsa_get_public_key65(&cnist256p1.nist256p1,
                                     <const uint8_t *>secret_key, out65)
        return PyBytes_FromStringAndSize(<char *>out65, 65)


def nist256p1_sign(secret_key, digest, compressed: bool = True) -> bytes:
    if len(secret_key) != 32:
        raise ValueError('Invalid length of secret key')
    if len(digest) != 32:
        raise ValueError('Invalid length of digest')
    cdef uint8_t out[65]
    cdef uint8_t pby
    if 0 != ecdsa.ecdsa_sign_digest(&cnist256p1.nist256p1,
                                    <const uint8_t *>secret_key,
                                    <const uint8_t *>digest,
                                    out + 1, &pby, NULL):
        raise ValueError('Signing failed')
    out[0] = 27 + pby + compressed * 4
    return PyBytes_FromStringAndSize(<char *>out, 65)


def nist256p1_verify(public_key, signature, digest) -> bool:
    pk_len = len(public_key)
    if pk_len != 33 and pk_len != 65:
        raise ValueError('Invalid length of public key')
    sig_len = len(signature)
    if sig_len != 64 and sig_len != 65:
        raise ValueError('Invalid length of signature')
    cdef int offset = sig_len - 64
    dig_len = len(digest)
    if dig_len != 32:
        raise ValueError('Invalid length of digest')
    sig_with_offset = signature[offset:]
    res = ecdsa.ecdsa_verify_digest(&cnist256p1.nist256p1,
                                    <const uint8_t *>public_key,
                                    <const uint8_t *>sig_with_offset,
                                    <const uint8_t *>digest)
    return res == 0


def nist256p1_verify_recover(signature, digest) -> bytes:
    sig_len = len(signature)
    if sig_len != 65:
        raise ValueError('Invalid length of signature')
    dig_len = len(digest)
    if dig_len != 32:
        raise ValueError('Invalid length of digest')
    cdef uint8_t recid = (<const uint8_t>signature[0]) - 27
    if recid >= 8:
        raise ValueError('Invalid recid in signature')
    cdef int compressed = (recid >= 4)
    recid &= 3
    cdef uint8_t out[65]

    sig_with_offset = signature[1:]
    if 0 == ecdsa.ecdsa_recover_pub_from_sig(&cnist256p1.nist256p1, out,
                                             <const uint8_t *>sig_with_offset,
                                             <const uint8_t *>digest, recid):
        if compressed:
            out[0] = 0x02 | (out[64] & 1)
            return PyBytes_FromStringAndSize(<char *>out, 33)
        return PyBytes_FromStringAndSize(<char *>out, 65)
    return None


def nist256p1_multiply(secret_key, public_key) -> bytes:
    sk_len = len(secret_key)
    if sk_len != 32:
        raise ValueError('Invalid length of secret key')
    pk_len = len(public_key)
    if pk_len != 33 and pk_len != 65:
        raise ValueError('Invalid length of public key')
    cdef uint8_t out[65]
    if 0 != ecdsa.ecdh_multiply(&cnist256p1.nist256p1,
                                <const uint8_t *>secret_key,
                                <const uint8_t *>public_key, out):
        raise ValueError('Multiply failed')

    return PyBytes_FromStringAndSize(<char *>out, 65)


class nist256p1:
    generate_secret = nist256p1_generate_secret
    publickey = nist256p1_publickey
    sign = nist256p1_sign
    verify = nist256p1_verify
    verify_recover = nist256p1_verify_recover
    multiply = nist256p1_multiply


# curve25519 implementation
include 'ed25519.pxi'

cimport ed25519 as ced25519


def curve25519_generate_secret() -> bytes:
    cdef uint8_t out[32]
    random_buffer(out, 32)
    out[0] &= 248
    out[31] &= 127
    out[31] |= 64
    return PyBytes_FromStringAndSize(<char *>out, 32)


def curve25519_publickey(secret_key) -> bytes:
    if len(secret_key) != 32:
        raise ValueError('Invalid length of secret key')

    cdef uint8_t out[32]
    ced25519.curve25519_scalarmult_basepoint(<uint8_t *>out,
                                                <const uint8_t *>secret_key)
    return PyBytes_FromStringAndSize(<char *>out, 32)


def curve25519_multiply(secret_key, public_key) -> bytes:
    sk_len = len(secret_key)
    if sk_len != 32:
        raise ValueError('Invalid length of secret key')
    pk_len = len(public_key)
    if pk_len != 32:
        raise ValueError('Invalid length of public key')
    cdef uint8_t out[32]
    ced25519.curve25519_scalarmult(<uint8_t *>out,
                                      <const uint8_t *>secret_key,
                                      <const uint8_t *>public_key)

    return PyBytes_FromStringAndSize(<char *>out, 32)


class curve25519:
    generate_secret = curve25519_generate_secret
    publickey = curve25519_publickey
    multiply = curve25519_multiply


# ed25519 implementation
cimport ed25519 as ced25519


def mod_ed25519_generate_secret() -> bytes:
    cdef uint8_t out[32]
    random_buffer(out, 32)
    out[0] &= 248
    out[31] &= 127
    out[31] |= 64
    return PyBytes_FromStringAndSize(<char *>out, 32)


def mod_ed25519_publickey(secret_key, compressed: bool = True) -> bytes:
    if len(secret_key) != 32:
        raise ValueError('Invalid length of secret key')

    cdef uint8_t out[32]
    ced25519.ed25519_publickey(<uint8_t *>secret_key,
                               <uint8_t *>out)
    return PyBytes_FromStringAndSize(<char *>out, 32)


def mod_ed25519_sign(secret_key, message, hasher: str = '') -> bytes:
    if len(secret_key) != 32:
        raise ValueError('Invalid length of secret key')
    msg_len = len(message)
    if msg_len == 0:
        raise ValueError('Empty data to sign')
    cdef ed25519_public_key pk
    sk = secret_key
    cdef uint8_t out[64]
    if len(hasher) > 0:
        if hasher != 'keccak':
            raise ValueError('Unknown hash function')
        raise NotImplementedError('Keccak hashing is not implemented')
    else:
        ced25519.ed25519_publickey(<uint8_t *>sk, pk)
        ced25519.ed25519_sign(<uint8_t *>message, msg_len,
                              <uint8_t *>sk,
                              pk, <uint8_t *>out)

    return PyBytes_FromStringAndSize(<char *>out, 64)


def mod_ed25519_verify(public_key, signature, message):
    pk_len = len(public_key)
    if pk_len != 32:
        raise ValueError('Invalid length of public key')
    sig_len = len(signature)
    if sig_len != 64:
        raise ValueError('Invalid length of signature')
    msg_len = len(message)
    if msg_len == 0:
        raise ValueError('Empty data to verify')
    res = ced25519.ed25519_sign_open(<uint8_t *>message, msg_len,
                                     <uint8_t *>public_key,
                                     <uint8_t *>signature)
    return res == 0


def mod_ed25519_cosi_combine_publickeys(public_keys):
    pklen = len(public_keys)
    if pklen > 15:
        raise ValueError('Can\'t combine more than 15 public keys')
    cdef ed25519_public_key pks[15]
    for i, k in enumerate(public_keys):
        len_k = len(k)
        if len_k != 32:
            raise ValueError('Invalid length of public key')
        memcpy(pks[i], <uint8_t *>k, len_k)
    cdef uint8_t out[32]
    res = ced25519.ed25519_cosi_combine_publickeys(<uint8_t *>out,
                                                   pks, pklen)
    if res != 0:
        raise ValueError('Error combining public keys')

    return PyBytes_FromStringAndSize(<char *>out, 32)


def mod_ed25519_cosi_combine_signatures(R, signatures):
    sigr_len = len(R)
    if sigr_len != 32:
        raise ValueError('Invalid length of R')
    siglen = len(signatures)
    if siglen > 15:
        raise ValueError('Can\'t combine more than 15 COSI signatures')
    cdef ed25519_cosi_signature sigs[15]
    for i, s in enumerate(signatures):
        len_s = len(s)
        if len_s != 32:
            raise ValueError('Invalid length of COSI signature')
        memcpy(sigs[i], <uint8_t *>s, len_s)

    cdef uint8_t out[64]
    ced25519.ed25519_cosi_combine_signatures(<uint8_t *>out,
                                             <uint8_t *>R,
                                             sigs, siglen)

    return PyBytes_FromStringAndSize(<char *>out, 64)


def mod_ed25519_cosi_sign(secret_key, message, nonce, sigR, combined_pubkey):
    sk_len = len(secret_key)
    if sk_len != 32:
        raise ValueError('Invalid length of secret key')
    nonce_len = len(nonce)
    if nonce_len != 32:
        raise ValueError('Invalid length of nonce')
    sigr_len = len(sigR)
    if sigr_len != 32:
        raise ValueError('Invalid length of R')
    pk_len = len(combined_pubkey)
    if pk_len != 32:
        raise ValueError('Invalid length of aggregated public key')
    cdef uint8_t out[32]
    msg_len = len(message)
    ced25519.ed25519_cosi_sign(<uint8_t *>message, msg_len,
                               <uint8_t *>secret_key,
                               <uint8_t *>nonce,
                               <uint8_t *>sigR,
                               <uint8_t *>combined_pubkey,
                               <uint8_t *>out)

    return PyBytes_FromStringAndSize(<char *>out, 32)


class ed25519:
    generate_secret = mod_ed25519_generate_secret
    publickey = mod_ed25519_publickey
    sign = mod_ed25519_sign
    verify = mod_ed25519_verify
    cosi_combine_publickeys = mod_ed25519_cosi_combine_publickeys
    cosi_combine_signatures = mod_ed25519_cosi_combine_signatures
    cosi_sign = mod_ed25519_cosi_sign


# cosi implementation
include 'rfc6979.pxi'

cimport rfc6979 as crfc6979


def cosi_cosi_commit(private_key, data):
    if data is None or len(data) < 1:
        raise ValueError('No data provided')

    cdef uint8_t nonce[32]
    cdef uint8_t commitment[32]
    cdef uint8_t pubkey[32]
    cdef rfc6979_state rng
    sha256_Raw(<uint8_t *>data, len(data), nonce)
    crfc6979.init_rfc6979(<uint8_t *>private_key, nonce, &rng)
    generate_rfc6979(nonce, &rng)
    ed25519_publickey(nonce, commitment)
    ed25519_publickey(<uint8_t *>private_key, pubkey)
    return (PyBytes_FromStringAndSize(<char *>commitment, 32),
            PyBytes_FromStringAndSize(<char *>pubkey, 32))


def cosi_cosi_sign(private_key, data, global_commitment, global_pubkey):
    if data is None or len(data) < 1:
        raise ValueError('No data provided')
    if global_commitment is None or len(global_commitment) != 32:
        raise ValueError('Lengt of global_commitment is not 32')
    if global_pubkey is None or len(global_pubkey) != 32:
        raise ValueError('Lengt of global_pubkey is not 32')

    cdef uint8_t nonce[32]
    cdef rfc6979_state rng
    cdef uint8_t signature[32]
    sha256_Raw(<uint8_t *>data, len(data), nonce)
    crfc6979.init_rfc6979(<uint8_t *>private_key, nonce, &rng)
    generate_rfc6979(nonce, &rng)
    ced25519.ed25519_cosi_sign(<uint8_t *>data, len(data),
                               <uint8_t *>private_key,
                               <uint8_t *>nonce,
                               <uint8_t *>global_commitment,
                               <uint8_t *>global_pubkey,
                               <uint8_t *>signature)

    return PyBytes_FromStringAndSize(<char *>signature, 32)

class cosi:
    cosi_commit = cosi_cosi_commit
    cosi_sign = cosi_cosi_sign
