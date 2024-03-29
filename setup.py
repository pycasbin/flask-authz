from setuptools import setup, find_packages
from os import path
import configparser

desc_file = "README.md"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, desc_file), encoding="utf-8") as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

# get current version for download_url
config = configparser.RawConfigParser()
config.read("setup.cfg")
download_v = dict(config.items("metadata")).get("version")


setup(
    name="flask-authz",
    author=["Yang Luo", "Sciencelogic"],
    author_email="hsluoyz@gmail.com",
    description="An authorization middleware for Flask that supports ACL, RBAC, ABAC, based on Casbin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pycasbin/flask-authz",
    keywords=[
        "flask",
        "pycasbin",
        "casbin",
        "auth",
        "authz",
        "acl",
        "rbac",
        "abac",
        "access control",
        "authorization",
        "permission",
    ],
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=install_requires,
    python_requires=">=3.5",
    data_files=[desc_file],
    include_package_data=True,
    dependency_links=dependency_links,
    download_url="https://github.com/pycasbin/flask-authz/tarball/v" + download_v,
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
