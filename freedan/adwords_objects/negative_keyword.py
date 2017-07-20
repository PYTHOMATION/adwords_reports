class NegativeKeyword:
    """ Negative Keywords are used to Block traffic in AdWords.
    Currently this class only takes care of AdGroup level negative Keywords.
    However, they can also be on Campaign level or in a shared library (even cross account)
    """
    def __init__(self, text, match_type):
        self.text = text
        self.match_type = match_type
        assert match_type in ("EXACT", "PHRASE", "BROAD")

    def add_on_adgroup_operation(self, adgroup_id):
        """ Add negative Keyword on AdGroup """
        operation = {
            'xsi_type': 'AdGroupCriterionOperation',
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'NegativeAdGroupCriterion',
                'adGroupId': adgroup_id,
                'criterion': {
                    'xsi_type': 'Keyword',
                    'matchType': self.match_type,
                    'text': self.text
                }
            }
        }
        return operation

    @staticmethod
    def delete_on_adgroup_operation(adgroup_id, keyword_id):
        """ Remove negative Keyword from AdGroup """
        operation = {
            'xsi_type': 'AdGroupCriterionOperation',
            'operator': 'REMOVE',
            'operand': {
                'xsi_type': 'NegativeAdGroupCriterion',
                'adGroupId': adgroup_id,
                'criterion': {
                    'id': keyword_id
                }
            }
        }
        return operation
