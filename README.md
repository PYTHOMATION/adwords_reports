# AdWords Reports
[![Build Status](https://travis-ci.org/SaturnFromTitan/adwords_reports.svg?branch=master)](https://travis-ci.org/SaturnFromTitan/adwords_reports)
[![codecov](https://codecov.io/gh/SaturnFromTitan/adwords_reports/branch/master/graph/badge.svg)](https://codecov.io/gh/SaturnFromTitan/adwords_reports)

## Description
`adwords_reports` is a library to quickly and easily receive cross-account reports from Google AdWords.

## Getting started
1. You can install `adwords_reports` using `pip`:

    `$ pip install adwords_reports`

or using `git`:

    `$ pip install git+https://github.com/SaturnFromTitan/adwords_reports.git`

1. Get access to AdWords API and cache all credential information in a .yaml file.
    * [Google's tutorial for authenticating with their API](https://www.youtube.com/watch?v=yaDlZMfYWkg&list=PLOU2XLYxmsII2PCvm73bwxRCu2g_dyp67&index=2) 
    * [Google's client library for python](https://github.com/googleads/googleads-python-lib)
    * You'll need to pass the path to this file to the Client for authentication:
    
    ```
    from adwords_reports import Client
    
    credentials_path = "adwords_credentials.yaml"
    client = Client(credentials_path)
    ```
1. Try to run the code in *examples/account_hierarchy.py* to see if everything is working.
    * Have a look at the other examples as well. This is the best place to get you up to speed.
1. For more detailed information on report types, available fields etc. please refer to the [Google's
      official documentation](https://developers.google.com/adwords/api/docs/appendix/reports).

## Technology
* The library currently supports Python 2.7 and 3.5+
* All reports are returned as [pandas](https://github.com/pandas-dev/pandas) DataFrames - the standard tool to analyse data in Python
* Tests are written with [pytest](https://github.com/pytest-dev/pytest).

## Who do I talk to?
The project was launched and is currently maintained by me, [Martin Winkel](https://www.linkedin.com/in/martin-winkel-90678977).

## Contribute
Contributors are very welcome! Just file an issue or pull request.
