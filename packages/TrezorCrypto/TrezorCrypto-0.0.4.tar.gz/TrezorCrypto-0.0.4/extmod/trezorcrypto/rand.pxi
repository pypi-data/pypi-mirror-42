# cython: language_level=3

from libc.stdint cimport uint32_t, uint8_t

cdef extern from "rand.h":
    uint32_t random32()
    void random_buffer(uint8_t *buf, size_t len)

    uint32_t random_uniform(uint32_t n)
    void random_permute(char *buf, size_t len)
