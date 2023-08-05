from pysam.libcalignedsegment cimport AlignedSegment


cdef extern from "strnum_cmp.c":
    int strnum_cmp(const char *_a, const char *_b)

cpdef int _compare_read_names(str a, str b):
    return strnum_cmp(a.encode(), b.encode())

cpdef int _compare_sort_with_queryname(AlignedSegment a, str queryname):
    return strnum_cmp(pysam_bam_get_qname(a._delegate), queryname.encode())

cpdef int _compare_sort(AlignedSegment a, AlignedSegment b):
    """
    Compare ``AlignedSegment`` a with ``AlignedSegment`` b by read name using the htslib sort rules.

    Returns 0 if readnames match, -1 if a sorts before b, 1 if b sorts before a.
    """
    return strnum_cmp(pysam_bam_get_qname(a._delegate), pysam_bam_get_qname(b._delegate))
