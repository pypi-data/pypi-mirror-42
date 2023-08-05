# cython: language_level=3

from libc.stdint cimport uint16_t, uint8_t, uint32_t

cdef extern from "bip39.h":
    char* mnemonic_generate(int strength)
    uint16_t* mnemonic_generate_indexes(int strength)
    char* mnemonic_from_data(uint8_t* data, int len)
    uint16_t* mnemonic_from_data_indexes(uint8_t* data, int len)
    int mnemonic_check(char* mnemonic)
    int mnemonic_to_entropy(char* mnemonic, uint8_t* entropy)
    ctypedef void (*_mnemonic_to_seed_progress_callback_ft)(uint32_t current, uint32_t total)
    void mnemonic_to_seed(char* mnemonic, char* passphrase, uint8_t seed[], _mnemonic_to_seed_progress_callback_ft progress_callback)
    char** mnemonic_wordlist()
