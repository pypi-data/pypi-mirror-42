# coding: utf-8

from setuptools import setup


version = open("VERSION", "rb").read().strip().decode("ascii")

setup(
    name="ssss",
    version=version,
    description="Pure Python Shamir's secret sharing scheme implementation",
    long_description=open("README", "rb").read().decode("utf-8"),
    author="Sergey Matveev",
    author_email="stargrave@stargrave.org",
    url="https://git.cypherpunks.ru/cgit.cgi/pyssss.git/",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    py_modules=["ssss"],
)
