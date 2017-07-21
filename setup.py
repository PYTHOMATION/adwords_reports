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
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


PACKAGES = [
    "freedan",
    "freedan.adwords_objects",
    "freedan.adwords_services",
    "freedan.other_services"
]

DEPENDENCIES = [
    "googleads",
    "pandas",
    "google-api-python-client",
    "pygsheets",
    "unidecode",
    "xlsxwriter"
]

CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.6"
]

setuptools.setup(
    name="freedan",
    description="Convenient and fast API for Google AdWords utilizing pandas",
    url="https://github.com/SaturnFromTitan/Freedan",
    version=find_version("freedan", "__init__.py"),
    packages=PACKAGES,
    license="Apache License 2.0",
    install_requires=DEPENDENCIES,
    classifiers=CLASSIFIERS,
    author="Martin Winkel",
    author_email="martin.winkel.pps@gmail.com"
)
