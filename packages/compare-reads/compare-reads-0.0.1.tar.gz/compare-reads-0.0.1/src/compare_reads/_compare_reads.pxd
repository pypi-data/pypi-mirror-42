import pysam
from pysam.libchtslib cimport *

cdef int strnum_cmp(const char *_a, const char *_b)

cdef extern from "htslib_util.h":
    bam1_t * pysam_bam_update(bam1_t * b,
                              size_t nbytes_old,
                              size_t nbytes_new,
                              uint8_t * pos)
    char * pysam_bam_get_qname(bam1_t * b)
