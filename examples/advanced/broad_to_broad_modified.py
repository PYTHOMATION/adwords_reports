import ast

import freedan
from freedan import Keyword, KeywordFinalUrl


def broad_to_broad_modified(path_credentials, is_debug):
    """
    A script that will look for (partially) "real" broad keywords and convert them to broad modified.

    It's good practise to avoid real broad keywords in your adwords accounts since the targeting is hard to control and
    it's very likely that your ad is showing for very unrelated searches.

    CAUTION: Since you can't change the text of a keyword in adwords, the script will delete the old keyword and
             add a new one with the fixed text. This means history for those keywords will be reset.
    CAUTION2: The new keywords will by default use https
    :param path_credentials: str, path to your adwords credentials file
    :param is_debug: bool
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        real_broads = identify_real_broads(adwords_service)

        operations = build_operations(real_broads)
        adwords_service.upload(operations, is_debug=is_debug, method="batch")


def build_operations(real_broads):
    """ You can't update keyword texts, therefore every keyword has to be deleted and recreated with the right text
    :param real_broads: DataFrame
    :return: tuple of 2 lists of operations
    """
    add_operations = list()
    del_operations = list()
    for index, row in real_broads.iterrows():
        # fetch current settings of keyword to create new one
        adgroup_id = int(row["AdGroupId"])
        keyword_id = int(row["Id"])
        match_type = row["KeywordMatchType"].upper()
        micro_bid = int(row["CpcBid"])
        status = row["Status"].upper()
        new_text = Keyword.to_broad_modified(row["Criteria"])
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


def identify_real_broads(adwords_service):
    """ Download all keywords and identify the ones with missing pluses
    :param adwords_service: AdWordsService object
    :return: DataFrame
    """
    fields = [
        "AdGroupName", "AdGroupId", "Criteria", "Id",
        "Status", "CpcBid", "KeywordMatchType", "FinalUrls"
    ]
    predicates = [{
        "field": "KeywordMatchType",
        "operator": "EQUALS",
        "values": "BROAD"
    }, {
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

    is_real_broad = keyword_report["Criteria"].apply(Keyword.is_real_broad)
    real_broads = keyword_report[is_real_broad]
    return real_broads


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    broad_to_broad_modified(adwords_credentials_path, is_debug=True)
