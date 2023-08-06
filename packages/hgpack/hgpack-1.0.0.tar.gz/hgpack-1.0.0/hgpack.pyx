# This is a Cython file which provides an interface to C++ code

# Authors: Daniel Gribel, Lorenzo Saraiva and Thibaut Vidal
# Contact: dgribel@inf.puc-rio.br

from libcpp.vector cimport vector

# distutils: language = c++
# distutils: sources = HGMeans.cpp

cdef extern from "HGMeans.h":
    cdef cppclass HGMeans:
        HGMeans()
        void Go(char*, int, int, int, vector[int])

cdef class PyHGMeans:
    cdef HGMeans *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self):
        self.thisptr = new HGMeans()
    def __dealloc__(self):
        del self.thisptr
    def Go(self, filename, size_population, it, evaluation, list_clusters):
        self.thisptr.Go(filename, size_population, it, evaluation, list_clusters)