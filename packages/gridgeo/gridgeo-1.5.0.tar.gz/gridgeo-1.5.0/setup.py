from pathlib import Path

from setuptools import setup

import versioneer

rootpath = Path(__file__).parent.absolute()


def read(*parts):
    return open(rootpath.joinpath(*parts), "r").read()


long_description = "{}\n{}".format(read("README.rst"), read("CHANGES.txt"))
LICENSE = read("LICENSE.txt")

with open("requirements.txt") as f:
    require = f.readlines()
install_requires = [r.strip() for r in require]

setup(
    name="gridgeo",
    version=versioneer.get_version(),
    license=LICENSE,
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
    ],
    description=(
        "Convert UGRID, SGRID, and some non-compliant ocean model grids to geo-like objects"
    ),  # noqa
    url="https://github.com/pyoceans/gridgeo",
    platforms="any",
    keywords=["geojson", "shapefile", "ocean models", "ugrid", "sgrid"],
    install_requires=install_requires,
    packages=["gridgeo"],
    tests_require=["pytest"],
    cmdclass=versioneer.get_cmdclass(),
    author=["Filipe Fernandes"],
    author_email="ocefpaf@gmail.com",
    entry_points={"console_scripts": ["gridio = gridgeo.gridio:main"]},
)
