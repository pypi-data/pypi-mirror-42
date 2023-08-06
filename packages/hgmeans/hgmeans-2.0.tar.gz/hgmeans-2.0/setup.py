from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    name = "hgmeans",
    version = "2.0",
    include_package_data = True,
    author = "Daniel Gribel",
    author_email = "dgribel@inf.puc-rio.br",
    url = "https://github.com/danielgribel/hg-means",
    description = "HG-means clustering for minimum sum-of-squares formulation",
    long_description = long_desc,
    # long_description_content_type = long_desc,
    keywords = "clustering optimization",
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
    ],
    ext_modules = [Extension(
            "hgmeans", [
                "hgmeans.pyx", 
                "hgmeans/HGMeans.cpp",
                "hgmeans/GeneticOperations.cpp",
                "hgmeans/MathUtils.cpp",
                "hgmeans/Solution.cpp",
                "hgmeans/hamerly/dataset.cpp",
                "hgmeans/hamerly/general_functions.cpp",
                "hgmeans/hamerly/hamerly_kmeans.cpp",
                "hgmeans/hamerly/kmeans.cpp",
                "hgmeans/hamerly/original_space_kmeans.cpp",
                "hgmeans/hamerly/triangle_inequality_base_kmeans.cpp"
            ],
            include_dirs=["hgmeans"],
            depends=["hgmeans/HGMeans.h"],
            language="c++",
            extra_compile_args=["-g", "-O3", "-std=c++11"]
    )]
)
