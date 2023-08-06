from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst")) as f:
    long_description = f.read()

version = "0.0.5"

setup(
    name="dialogue.multi-method",
    version=version,
    maintainer="Hugo Duncan",
    maintainer_email="hugo.duncan@dialogue.co",
    url="https://github.com/dialoguemd/multi-method",
    long_description=long_description,
    packages=["dialogue.multi_method"],
    install_requires=[],
    extras_require={
        "dev": [
            "black",
            "isort",
            "pre-commit",
            "pytest",
            "pytest-watch",
            "python-semantic-release",
        ],
        "test": ["codecov", "pylama", "pytest", "pytest-cov", "tox"],
    },
)
