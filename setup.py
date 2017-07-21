from setuptools import setup


PACKAGES = [
    'freedan',
    'freedan.adwords_objects',
    'freedan.adwords_services',
    'freedan.other_services'
]

DEPENDENCIES = [
    'googleads',
    'pandas',
    'google-api-python-client',
    'pygsheets',
    'unidecode',
    'xlsxwriter'
]

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.6'
]

setup(
    name='freedan',
    description='Convenient and fast API for Google AdWords utilizing pandas',
    url='https://github.com/SaturnFromTitan/Freedan',
    version='0.1.4',
    packages=PACKAGES,
    license='Apache License 2.0',
    install_requires=DEPENDENCIES,
    classifiers=CLASSIFIERS,
    author='Martin Winkel',
    author_email='martin.winkel.pps@gmail.com'
)
