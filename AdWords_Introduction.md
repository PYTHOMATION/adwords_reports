# AdWords Context #
### Concepts ###
Google's search engine is a great place to run advertisement, since users are already actively searching for something.
Imagine you are a travel company and a user types "cheap flight mallorca" into google's search bar:
The user intend to book a trip is already be very high, therefore it's more likely that the user will convert on your website, than if you just randomly target people for instance in a Facebook newsfeed.
Therefore Google Search can often be very cost efficient.

Based on the **SearchQuery** - the text a person entered into Google's search bar - you try to identify users that are very likely to convert with your product.
You therefore create **Keywords** inside Google AdWords that consist of a keyword text, a bid and some other properties.
Those keywords "catch" certain SearchQueries and are connected to an Ad. If the user clicks on this Ad he's sent to our website. Google charges per Click, which is also known as a ppc model.

Normally a lot of different companies want to buy clicks of a single user, so Google created multiple spots for purchased advertisement.  
In general there are 4 paid spots above the organic search results. However, there can be additional advertisement at the bottom of the page and other pages as well, but they're not very relevant.

To determine who get's the top position for a search Google designed an **Auction** system.
Here every company gets a score called **AdRank** which is mainly determined by a **Bid** and a **QualityScore**.
The bid is for Google to earn shit loads of money and the QualityScore makes sure that ads are not too spammy, the ads are relevant to the search and the user experience remains good.
QualityScore consists of three parts: expected CTR, Ad relevance and expected landing page experience 

### Objects in AdWords  ###
* Account
    * ... is basically just a container for Campaigns
    * ... is the most high level container in AdWords API
        * (In the UI there are 'MCC's which group together accounts, but in the API they don't exist)
    * The following settings can be specified on account level
        * Currency
        * Time Zone
        * Billing
* Campaign
    * ... is a container for AdGroups
    * The following settings can be specified on campaign level
        * Languages
        * Locations
        * Budgets
        * Ad Extensions
        * CampaignType
            * i.e. where Ads are shown. Google Search/Search Partners/Google Display Network/...
        * Bid multiplier per device
            * Can also be set on AdGroup level (preferred)
        * Ad Schedule
            * Bid multipliers based on weekdays or hours
* AdGroup
    * ... is a container for neg. Keywords and Ads
    * The following settings can be specified on adgroup level
        * Device based bid multipliers
* positive Keyword consists of 
    * Text
    * MatchType
        * Determines which search queries can be matched by the keyword
        * Exact - SearchQuery == KeywordText (or close variant, i.e. plural, typos, ...)
        * Phrase - SearchQuery contains KeywordText
        * Broad Modified - SearchQuery contains all words of the KeywordText
        * Broad - Like Broad Modified, but synonyms are also allowed
    * Bid
        * Amount in Euro that's used in Google's auction system
    * FinalUrl
        * Destination if somebody clicks on a link
* negative Keywords
    * ... used to block traffic. They can be created on different levels for different purposes:
        * AdGroup - Don't block the traffic, but reallocate it to another AdGroup. E.g. if a broad steals traffic from a related exact keyword
        * Campaign - Don't block the traffic, but reallocate it to another Campaign. E.g. triggered by wrong route type
        * Account (via SharedSet) - Block traffic because it's not relevant to our business
    * MatchTypes
        * MatchTypes work slightly differnt for negative keywords:
        * There is no close variant matching, i.e. negative "bus düsseldorf" won't block "bus dusseldorf"
        * The "real" broad works like broad modified
* Ad
    * ... loosely connected to Keywords of the same AdGroup. I.e. AdWords will (randomly) select an Ad from the same AdGroup as the keyword is in.
    * Ad Types
        * There are two different types of Ads for Search:
            * Extended TextAds (ETAs) - Newest Ad Format released at end 2016. In general you can occupy more space on the search result page 
            * Standard TextAds - deprecated since January. You can't create them anymore, but there are some old ones in the accounts that still serve (no new ad could beat them so far in tests)
    * Final Urls
        * Ads also have a final url, but they are not used for directing customers to landing pages
        * Currently the only purpose is to have a common key for ad test evaluations
* Shared Sets (sometimes "Shared Libraries")
    * ... usually this refers to a collection of negative keywords that are applied across multiple accounts/campaigns

### Special Concepts ###
* Ad Extensions
    * Ads can have special extensions that are shown if your AdRank is much higher than the one of the competition
    * Try to enter "goeuro" into Google and have a look
* Low Search Volume
    * Google automatically pauses some of your keywords if there are too few searches recently.
    * Afaik they don't reveal what "too few searches" means exactly
* Temporary Ids for batch uploads in API
    * Negative integers
    * This way you can send campaign, adgroup, keyword, ad, ... operations in one upload. Otherwise you'd need to
        1. upload campaigns
        1. fetch their ids
        1. then create adgroups
        1. fetch their ids
        1. etc...
