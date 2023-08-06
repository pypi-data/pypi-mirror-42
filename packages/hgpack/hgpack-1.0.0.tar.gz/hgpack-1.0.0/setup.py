from setuptools import setup, Extension

setup(
    name = "hgpack",
    version = "1.0.0",
    author="Daniel Gribel",
    author_email="dgribel@inf.puc-rio.br",
    description="HG-means clustering package",
    keywords = "clustering optimization",
    # ext_modules = [Extension("edlib",
    #                          ["edlib.bycython.c", "edlib/src/edlib.cpp"],
    #                          include_dirs=["edlib/include"])]
    ext_modules = [Extension(
            "hgpack", [
                "hgpack.pyx", 
                "hgpack/src/HGMeans.cpp",
                "hgpack/src/GeneticOperations.cpp",
                "hgpack/src/MathUtils.cpp",
                "hgpack/src/Solution.cpp",
                "hgpack/src/hamerly/dataset.cpp",
                "hgpack/src/hamerly/general_functions.cpp",
                "hgpack/src/hamerly/hamerly_kmeans.cpp",
                "hgpack/src/hamerly/kmeans.cpp",
                "hgpack/src/hamerly/original_space_kmeans.cpp",
                "hgpack/src/hamerly/triangle_inequality_base_kmeans.cpp"
            ],
            include_dirs=["hgpack/src"],
            language="c++",
            extra_compile_args=["-std=c++11"]
        )]
        # cmdclass = {'build_ext': build_ext}
)
