import os
import io
import re
import setuptools


# Read version from __init__.py file of project
# Taken from https://packaging.python.org/guides/single-sourcing-package-version/
def read(*names, **kwargs):
    file_path = os.path.dirname(__file__)
    with io.open(
            os.path.join(file_path, *names),
            encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


PACKAGES = [
    "adwords_reports"
]

DEPENDENCIES = [
    "googleads",
    "pandas",
    "retrying"
]

CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.6"
]
KEYWORDS = [
    "data",
    "analytics",
    "api",
    "wrapper",
    "google",
    "adwords",
    "reports",
    "reporting"
]

setuptools.setup(
    name="adwords_reports",
    description="Pythonic wrapper of the Google AdWords API for easy reporting.",
    keywords=" ".join(KEYWORDS),
    author="Martin Winkel",
    author_email="martin.winkel.pps@gmail.com",
    url="https://github.com/SaturnFromTitan/adwords_reports",
    version=find_version("adwords_reports", "__init__.py"),
    packages=PACKAGES,
    install_requires=DEPENDENCIES,
    classifiers=CLASSIFIERS,
    license="Apache License 2.0"
)
