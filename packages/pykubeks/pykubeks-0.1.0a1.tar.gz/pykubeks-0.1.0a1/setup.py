import sys

from setuptools import setup, find_packages


with open("README.md") as fp:
    long_description = fp.read()

install_requires = [
    "requests>=2.12",
    "PyYAML",
    "six>=1.10.0",
    "tzlocal",
]

if sys.version_info < (3,):
    install_requires.extend([
        "ipaddress",
    ])

setup(
    name="pykubeks",
    version="0.1.0a1",
    description="Python client library for Kubernetes w/ EKS support",
    long_description=long_description,
    author="Steinn Eldjárn Sigurðarson",
    author_email="steinnes@gmail.com",
    license="Apache",
    url="https://github.com/steinnes/pykubeks",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        "httpie.plugins.transport.v1": [
            "httpie_pykube = pykube.contrib.httpie_plugin:PyKubeTransportPlugin"
        ],
    },
    install_requires=install_requires,
    extras_require={
        "gcp": [
            "google-auth",
            "jsonpath-ng",
        ]
    },
)
