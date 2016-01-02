from setuptools import setup, find_packages
import os

setup(
    name = "python-mongo-validator",
    version = "0.0.1",
    description = "Cerberus validation for pymongo",
    author = "Colton Leekley-Winslow",
    package_dir = {"":"src"},
    packages = find_packages("src"),
)
