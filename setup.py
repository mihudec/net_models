from setuptools import setup, find_packages

VERSION = "0.0.1"

setup(
    name="netcm",
    packages=find_packages(where="netcm"),
    package_dir={
        "": "netcm"
    },
    version=VERSION,
    author="Miroslav Hudec <http://github.com/mihudec>",
)