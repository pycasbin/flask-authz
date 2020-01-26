import setuptools

desc_file = "README.md"

with open(desc_file, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-authz",
    version="1.0.0",
    author="Yang Luo",
    author_email="hsluoyz@gmail.com",
    description="An authorization middleware for Flask that supports ACL, RBAC, ABAC, based on Casbin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pycasbin/flask-authz",
    keywords=["flask", "casbin", "auth", "authz", "acl", "rbac", "abac", "access control", "authorization", "permission"],
    packages=setuptools.find_packages(),
    install_requires=['casbin', 'flask', 'werkzeug'],
    python_requires=">=3.5",
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    data_files=[desc_file],
)
