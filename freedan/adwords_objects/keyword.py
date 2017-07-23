from freedan.adwords_services.adwords_service import AdWordsService
from freedan.adwords_objects.keyword_final_url import KeywordFinalUrl

MAX_WORDS_KEYWORD = 10
MAX_CHARS_KEYWORD = 80


class Keyword:
    """ Keywords utility model.
    Keywords ultimately determine the targeting in our accounts.
    Keywords consist of more than a text, they also have
        - match type
        - bid
        - final url
    """
    def __init__(self, text, match_type, max_cpc, final_url, convert_to_micro=True):
        self.text = text.lower()
        self.match_type = match_type.upper()
        self.max_cpc = AdWordsService.euro_to_micro(max_cpc) if convert_to_micro else max_cpc

        if isinstance(final_url, str):
            self.final_url = final_url
        elif isinstance(final_url, KeywordFinalUrl):
            self.final_url = final_url.final_url
        else:
            raise ValueError("Unexpected value for final url. Please provide string or KeywordFinalUrl object.")
        assert self.match_type in ("EXACT", "PHRASE", "BROAD")

    @staticmethod
    def is_real_broad(broad_text):
        """ assumes that broad modified contains +'s
        In a real broad one of the words doesn't start with a +
        """
        return any(not word.startswith("+") for word in broad_text.split())

    @staticmethod
    def to_broad_modified(broad):
        """ Add a '+' to the beginning of all words in a word group """
        broad_modified = " +".join([word.replace("+", "") for word in broad.split()])
        broad_modified = "+" + broad_modified
        return broad_modified.lower()

    def basic_checks(self):
        """ Check against limitation of AdWords """
        assert len(self.text) <= MAX_CHARS_KEYWORD
        assert len(self.text.split()) <= MAX_WORDS_KEYWORD

    def add_operation(self, adgroup_id, status="ENABLED", label_id=None):
        """ Add keyword to adgroup operation for adwords API """
        assert self.max_cpc >= 10000  # i.e. at least 1 cent
        self.basic_checks()

        operation = {
            "xsi_type": "AdGroupCriterionOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "BiddableAdGroupCriterion",
                "adGroupId": adgroup_id,
                "userStatus": status,
                "criterion": {
                    "xsi_type": "Keyword",
                    "text": self.text,
                    "matchType": self.match_type
                },
                "finalUrls": {
                    "urls": [self.final_url]
                },
                "biddingStrategyConfiguration": {
                    "bids": [
                        {
                            "xsi_type": "CpcBid",
                            "bid": {
                                "xsi_type": "Money",
                                "microAmount": self.max_cpc
                            }
                        }
                    ]
                }
            }
        }
        if label_id is not None:
            operation["operand"]["labels"] = [{
                "id": label_id
            }]
        return operation

    @staticmethod
    def delete_operation(adgroup_id, keyword_id):
        """ delete operation of a keyword """
        operation = {
            "xsi_type": "AdGroupCriterionOperation",
            "operator": "REMOVE",
            "operand": {
                "xsi_type": "BiddableAdGroupCriterion",
                "adGroupId": adgroup_id,
                "criterion": {
                    "id": keyword_id
                }
            }
        }
        return operation

    @staticmethod
    def set_bid(adgroup_id, keyword_id, bid, convert_to_micro=True):
        if convert_to_micro:
            bid = AdWordsService.euro_to_micro(bid)

        operation = {
            "xsi_type": "AdGroupCriterionOperation",
            "operator": "SET",
            "operand": {
                "xsi_type": "BiddableAdGroupCriterion",
                "adGroupId": adgroup_id,
                "criterion": {
                    "xsi_type": "Keyword",
                    "id": keyword_id,
                },
                "biddingStrategyConfiguration": {
                    "bids": [
                        {
                            "xsi_type": "CpcBid",
                            "bid": {
                                "xsi_type": "Money",
                                "microAmount": bid
                            }
                        }
                    ]
                }
            }
        }
        return operation
