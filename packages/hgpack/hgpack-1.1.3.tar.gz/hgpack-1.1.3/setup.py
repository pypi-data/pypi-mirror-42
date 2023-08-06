from setuptools import setup, Extension

setup(
    name = "hgpack",
    version = "1.1.3",
    include_package_data = True,
    author = "Daniel Gribel",
    author_email = "dgribel@inf.puc-rio.br",
    url = "https://github.com/danielgribel/hg-means",
    description = "HG-means clustering package",
    keywords = "clustering optimization",
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
            depends=["hgpack/src/HGMeans.h"],
            language="c++",
            extra_compile_args=["-g", "-O3", "-std=c++11"]
    )]
)
