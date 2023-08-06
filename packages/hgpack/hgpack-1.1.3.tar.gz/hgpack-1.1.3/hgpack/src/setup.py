from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(ext_modules=[Extension(
            "HGWrapper", [
                "HGWrapper.pyx", 
                "HGMeans.cpp",
                "GeneticOperations.cpp",
                "MathUtils.cpp",
                "Solution.cpp",
                "hamerly/dataset.cpp",
                "hamerly/general_functions.cpp",
                "hamerly/hamerly_kmeans.cpp",
                "hamerly/kmeans.cpp",
                "hamerly/original_space_kmeans.cpp",
                "hamerly/triangle_inequality_base_kmeans.cpp"
            ],
            language="c++",
            extra_compile_args=["-std=c++11"]
        )
    ],
    cmdclass = {'build_ext': build_ext}
)