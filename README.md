# PyAdWordsReports - The AdWords Reporting Framework
PyAdWordsReports is a framework to quickly receive cross-account reports from Google AdWords.

Previously this framework was delivering additional functionality for account creation, bidding, ad testing
and more. Sadly this overambitious goal resulted in overall sub-optimal design decisions, code quality and 
a too little testing suite.

Therefore the new goal of this frameowrk is to be the best and easiest to use reporting library for Google
AdWords. The additional functionality from previous versions might be added later in a separate framework. 

## Getting started
1. Install python 3.6.
    * Check out [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
    if you have an older version of python installed
1. You can install PyAdWordsReports using pip.

    `$ pip install py_adwords_reports`
1. Get access to AdWords API and cache all credential information in a .yaml file.
    * [Google's tutorial for authenticating with their API](https://www.youtube.com/watch?v=yaDlZMfYWkg&list=PLOU2XLYxmsII2PCvm73bwxRCu2g_dyp67&index=2) 
    * [Google's client library for python](https://github.com/googleads/googleads-python-lib)
    * You'll need to pass the path to this file to the AdWordsService object for authentication.
    
    ```
    from py_adwords_reports import AdWordsClient
    
    credentials_path = "adwords_credentials.yaml"
    client = AdWordsClient(credentials_path)
    ```
1. Try to run the code in *examples/basic/account_hierarchy.py* to see if everything is working.

## Technology
* Everything is built with Python. I'm using python 3.6. and didn't check for compatibility with earlier Python versions
    * According Raymond Hettinger's [great talk about dictionaries in python 3.6.](https://www.youtube.com/watch?v=p33CVV29OG8)
    you should consider updating anyway ;)
* All reports are returned as DataFrames - see [pandas](https://github.com/pandas-dev/pandas): The flexible, 
easy and powerful data analysis library for python
* Tests are intended to work with [pytest](https://github.com/pytest-dev/pytest).

## Examples
Please have a look at the example folder. Those scripts demonstrate the power and beauty of the
framework. Some of the advanced scripts might be ready for production as they are - so they might safe
you a lot of time. Let me know if you find them useful!

## Who do I talk to?
The project was launched and is currently maintained by me, [Martin Winkel](https://www.linkedin.com/in/martin-winkel-90678977):
 martin.winkel.pps@gmail.com.

## Contribute
Contributors are very welcome! There's still a lot of good stuff to build :)

If you wish to contribute file an issue, pull request or contact me please.
