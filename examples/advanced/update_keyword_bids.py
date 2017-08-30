import freedan
from freedan import Keyword

# an easy and fast way to receive those ids is the KEYWORDS_PERFORMANCE_REPORT
ADGROUP_ID = "INSERT_ID_HERE"
KEYWORD_ID = "INSERT_ID_HERE"
NEW_BID = "INSERT_BID_HERE"  # in regular amount, not micros


def update_keyword_bids(path_credentials, is_debug):
    """
    A script that will delete all empty Campaigns in all accounts.
    A Campaign is considered to be empty if it doesn't contain any AdGroups.

    :param path_credentials: str, path to your adwords credentials file
    :param is_debug: bool
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        operations = [
            Keyword.set_bid(adgroup_id=ADGROUP_ID, keyword_id=KEYWORD_ID, bid=NEW_BID)
        ]
        adwords_service.upload(operations, is_debug=is_debug)


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    update_keyword_bids(adwords_credentials_path, is_debug=True)
