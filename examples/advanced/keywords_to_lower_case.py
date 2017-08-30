import ast

import freedan
from freedan import Keyword, KeywordFinalUrl


def keywords_to_lower_case(path_credentials, is_debug):
    """
    A script that will look for (partially) non-lower case keywords and convert them to lower case.

    It's good practise to keep all your keywords lower case as adwords' serving is case insensitive, but keyword ids
    aren't. Therefore you might end up with duplications or other unwanted side effects, for instance when matching
    queries and existing keywords.

    CAUTION: Since you can't change the text of a keyword in adwords, the script will delete the old keyword and
             add a new one with the fixed text. This means history for those keywords will be reset.
    CAUTION2: The new keywords will by default use https in final url
    :param path_credentials: str, path to your adwords credentials file
    :param is_debug: bool
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        non_lower_case = identify_non_lower_case(adwords_service)

        operations = build_operations(non_lower_case)
        adwords_service.upload(operations, is_debug=is_debug, method="batch")


def build_operations(non_lower_case):
    """ You can't update keyword texts, therefore every keyword has to be deleted and recreated with the right text
    :param non_lower_case: DataFrame
    :return: tuple of 2 lists of operations
    """
    add_operations = list()
    del_operations = list()
    for index, row in non_lower_case.iterrows():
        # fetch current settings of keyword to create new one
        adgroup_id = int(row["AdGroupId"])
        keyword_id = int(row["Id"])
        match_type = row["KeywordMatchType"].upper()
        micro_bid = int(row["CpcBid"])
        status = row["Status"].upper()
        new_text = row["Criteria"].lower()
        final_url = ast.literal_eval(row["FinalUrls"])[0]  # breaks if no final url is set
        final_url = KeywordFinalUrl(final_url, https=True)

        # new keyword
        new_kw = Keyword(text=new_text, match_type=match_type, max_cpc=micro_bid, final_url=final_url)
        add_operation = new_kw.add_operation(adgroup_id, status=status)
        add_operations.append(add_operation)

        # deletion of flawed keyword
        del_operation = Keyword.delete_operation(adgroup_id=adgroup_id, keyword_id=keyword_id)
        del_operations.append(del_operation)
    return add_operations, del_operations


def identify_non_lower_case(adwords_service):
    """ Download all keywords and identify the ones with missing pluses
    :param adwords_service: AdWordsService object
    :return: DataFrame
    """
    fields = [
        "AdGroupName", "AdGroupId", "Criteria", "Id",
        "Status", "CpcBid", "KeywordMatchType", "FinalUrls"
    ]
    predicates = [{
        "field": "Status",
        "operator": "NOT_EQUALS",
        "values": "REMOVED"
    }, {
        "field": "AdGroupStatus",
        "operator": "NOT_EQUALS",
        "values": "REMOVED"
    }, {
        "field": "CampaignStatus",
        "operator": "NOT_EQUALS",
        "values": "REMOVED"
    }]

    keyword_report_def = adwords_service.report_definition("KEYWORDS_PERFORMANCE_REPORT", fields, predicates)
    keyword_report = adwords_service.download_report(keyword_report_def, include_0_imp=True)

    # CAUTION: one could try to use native python function str.islower()
    # but this results in undesired effects for Chinese
    is_not_lower_case = keyword_report["Criteria"] != keyword_report["Criteria"].str.lower()
    not_lower_case = keyword_report[is_not_lower_case]
    return not_lower_case


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    keywords_to_lower_case(adwords_credentials_path, is_debug=True)
