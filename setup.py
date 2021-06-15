from setuptools import setup, find_packages

VERSION = "0.1.4"

with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]

setup(
    name="net_models",
    packages=find_packages(),
    version=VERSION,
    author="Miroslav Hudec <http://github.com/mihudec>",
    description="Network Config Models",
    install_requires=reqs,
    include_package_data=True
)