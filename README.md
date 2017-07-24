# Freedan - The AdWords Automation Framework
Freedan is a framework to quickly create cross-account automation with Google AdWords.
Using it, one can easily automate big parts of manual day-to-day work, quickly test new ideas
to improve performance or even build sophisticated software solutions such as a custom bidding
algorithm.

## How does it compare to other AdWords automation solutions from Google?
Freedan provides an alternative to **UI Scripts**, **Power Editor** by building on top of the **native
Python client library** for Google AdWords.

Especially when accounts become large, the first two solutions tend to get slow and painful to use.
Compared to UI Scripts, you have the freedom to test and integrate the code to your existing code base.
Also, you won't encounter any of the limitations such as limited runtime, limited scheduling options,
operation limits etc. since you can host it on your own.

Freedan provides a simpler user interface for the most frequently used parts of the AdWords API, while
incorporating all best practises suggested by Google.

## Use cases
Common goals for freedan scripts:
* validate/adapt namings of accounts, campaigns, adgroups, ... > improve data quality
* delete old/empty campaigns, adgroups, ... > improve speed when working with Power Editor
* adjust bids > improve cost efficiency of accounts
* update ads > improve customer experience + raise CTR
* create negative keywords > reallocate search queries to more suitable keywords and/or block bad traffic
* create new accounts / add more keywords > Increase reach to target more customers

Expected workflow of those scripts:
1. gather custom input (cli, data warehouses, google drive, ...)
1. gather account information from AdWords
1. compute changes
1. upload updated parameters back to AdWords

## Getting started
1. For an introduction to AdWords refer to AdWords_Introduction.md
1. Install python 3.6.
    * Check out [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
    if you have an older version of python installed
1. You can install freedan using pip:

    `$ pip install freedan`
1. Get access to AdWords API and cache all credential information in a .yaml file
    * [Googles tutorial for authenticating with their API](https://www.youtube.com/watch?v=yaDlZMfYWkg&list=PLOU2XLYxmsII2PCvm73bwxRCu2g_dyp67&index=2) 
    * [Googles client library for python](https://github.com/googleads/googleads-python-lib)
    * You'll need to pass the path to this file to the AdWordsService object for authentication
    
    ```
    from freedan import AdWordsService
    
    credentials_path = "adwords_credentials.yaml"
    adwords_service = AdWordsService(credentials_path)
    ```
1. Try to run the code in *examples/basic/account_hierarchy.py* to see if everything is working

## Technology
* Everything is built with Python. I'm using python 3.6. and didn't check for compatibility with other Python versions
    * According Raymond Hettingers [great talk about dictionaries in python 3.6.](https://www.youtube.com/watch?v=p33CVV29OG8)
    you should consider updating anyway ;)
* All scripts heavily rely on the [pandas](https://github.com/pandas-dev/pandas): the flexible, 
easy and powerful data analysis library for python
* Tests are intended to work with [pytest](https://github.com/pytest-dev/pytest): a very easy,
yet powerful framework for testing

## Examples
Please have a look at the example folder. Those scripts demonstrate the power and beauty of the
framework. Some of the advanced scripts might be ready for production as they are - so they might safe
you a lot of time. Let me know if you find them useful!

## Who do I talk to?
The project was launched and is currently maintained by me, [Martin Winkel](https://www.linkedin.com/in/martin-winkel-90678977):
 martin.winkel.pps@gmail.com.
 
I recently relocated to Vancouver, BC, Canada.

## Bugs
If you've found a bug, please let me know. File an issue or send me an email.

## Contribute
Contributors are very welcome! There's still a lot of good stuff to build :)

If you find any important functionality missing, please let me know or create a
pull request.

## Future
The next big step will be the addition of placeholder methods to Account, Campaign, AdGroup and ETA.
You'll then be able to plug and play your unique business logic encoded in the names of those objects.
