from setuptools import setup, find_packages

VERSION = "0.1.1"

with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]

setup(
    name="netcm",
    packages=find_packages(include=["netcm"]),
    package_dir={
        "": "netcm"
    },
    version=VERSION,
    author="Miroslav Hudec <http://github.com/mihudec>",
    description="Network Config Models",
    install_requires=reqs,
    include_package_data=True
)