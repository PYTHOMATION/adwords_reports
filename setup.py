from distutils.core import setup


DEPENDENCIES = [
    'googleads', 'pandas', 'google-api-python-client',
    'pygsheets', 'unidecode', 'xlsxwriter'
]

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.6'
]

setup(
    name='freedan',
    version='0.1',
    packages=['freedan'],
    description='Convenient and fast API for Google AdWords utilizing pandas',
    url='https://github.com/SaturnFromTitan/Freedan',
    license='Apache License 2.0',
    author='Martin Winkel',
    author_email='martin.winkel.pps@gmail.com',
    install_requires=DEPENDENCIES,
    classifiers=CLASSIFIERS
)
