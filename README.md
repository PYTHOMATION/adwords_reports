# AdWords Reports
[![Build Status](https://travis-ci.org/SaturnFromTitan/adwords_reports.svg?branch=master)](https://travis-ci.org/SaturnFromTitan/adwords_reports)
[![codecov](https://codecov.io/gh/SaturnFromTitan/adwords_reports/branch/master/graph/badge.svg)](https://codecov.io/gh/SaturnFromTitan/adwords_reports)

## Description
AdWordsReports is a framework to quickly receive cross-account reports from Google AdWords.

Previously this framework was delivering additional functionality for account creation, bidding, ad testing
and more. Sadly this overambitious goal resulted in sub-optimal design decisions, code quality issues and 
too few tests.

Therefore the new goal of this framework is to be the best and easiest to use reporting library for Google
AdWords. The additional functionality from previous versions might be added later in form of a separate
library. 

## Getting started
1. Install python 3.6.
    * Check out [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
    if you have an older version of python installed
1. You can install AdWordsReports using pip.

    `$ pip install adwords_reports`
1. Get access to AdWords API and cache all credential information in a .yaml file.
    * [Google's tutorial for authenticating with their API](https://www.youtube.com/watch?v=yaDlZMfYWkg&list=PLOU2XLYxmsII2PCvm73bwxRCu2g_dyp67&index=2) 
    * [Google's client library for python](https://github.com/googleads/googleads-python-lib)
    * You'll need to pass the path to this file to the AdWordsService object for authentication.
    
    ```
    from adwords_reports import AdWordsClient
    
    credentials_path = "adwords_credentials.yaml"
    client = AdWordsClient(credentials_path)
    ```
1. Try to run the code in *examples/account_hierarchy.py* to see if everything is working.
    * Have a look at the other examples as well. This is the best place to get you up to speed.
1. For more detailed information on report types, available fields etc. please refer to the [Google's
      official documentation](https://developers.google.com/adwords/api/docs/appendix/reports).

## Technology
* Everything is written in Python. I'm using python 3.6.0 and didn't check for compatibility with earlier Python versions
    * According Raymond Hettinger's [great talk about dictionaries in python 3.6.](https://www.youtube.com/watch?v=p33CVV29OG8)
    you should consider updating anyway ;)
* All reports are returned as DataFrames - see [pandas](https://github.com/pandas-dev/pandas): The flexible, 
easy and powerful data analysis library for python
* Tests are intended to work with [pytest](https://github.com/pytest-dev/pytest).

## Who do I talk to?
The project was launched and is currently maintained by me, [Martin Winkel](https://www.linkedin.com/in/martin-winkel-90678977):
 martin.winkel.pps@gmail.com.

## Contribute
Contributers are very welcome! :) Just file an issue, pull request or contact me.
