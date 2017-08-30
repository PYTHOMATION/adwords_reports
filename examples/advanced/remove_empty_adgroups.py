import freedan
from freedan import AdGroup


def remove_empty_adgroups(path_credentials, is_debug):
    """
    A script that will delete all empty AdGroups in all accounts.
    An AdGroup is considered to be empty if it doesn't contain any keywords.
    Before you use it in production you might want to:
        - adapt the account selector
        - change the upload method
        - verify the script matches your needs, e.g. run it in debug mode and have a look into the resulting DataFrames
    Prospect: Adapt this script to
        - easily identify empty campaigns
        - or adgroups without ads
        - ...
    :param path_credentials: str, path to your adwords credentials file
    :param is_debug: bool
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        empty_adgroups = identify_empty_adgroups(adwords_service)
        # potentially save this DataFrame as a changelog

        operations = build_operations(empty_adgroups)
        adwords_service.upload(operations, is_debug=is_debug)


def build_operations(adgroups):
    """ Build delete operations for AdGroups
    :param adgroups: DataFrame
    :return: list of operations
    """
    operations = list()
    for index, row in adgroups.iterrows():
        adgroup_id = int(row["AdGroupId"])
        delete_operation = AdGroup.delete_operation(adgroup_id=adgroup_id)
        operations.append(delete_operation)
    return operations


def identify_empty_adgroups(adwords_service):
    """ Download all adgroups and identify which don't have Keywords
    :param adwords_service: AdWordsService object
    :return: DataFrame
    """
    # ignore deleted entities
    fields = ["CampaignName", "AdGroupName", "AdGroupId"]
    predicates = [{
        "field": "AdGroupStatus",
        "operator": "NOT_EQUALS",
        "values": "REMOVED"
    }, {
        "field": "CampaignStatus",
        "operator": "NOT_EQUALS",
        "values": "REMOVED"
    }]

    # define helper function since most arguments are equal for both reports
    def temp_report_definition(report_type):
        return adwords_service.report_definition(report_type, fields, predicates)

    # the adgroup report will contain all adgroups of the account
    adgroup_report_def = temp_report_definition("ADGROUP_PERFORMANCE_REPORT")
    all_adgroups = adwords_service.download_report(adgroup_report_def, include_0_imp=True)
    if all_adgroups.empty:  # skip rest if no adgroups in the account. otherwise merge later on triggers warning
        return all_adgroups

    # the keyword report will only contain adgroups belonging to keywords in the account
    keyword_report_def = temp_report_definition("KEYWORDS_PERFORMANCE_REPORT")
    keyword_adgroups = adwords_service.download_report(keyword_report_def, include_0_imp=True)

    # identify all adgroups in adgroup_report that are not in keyword_report
    # could also be done with set operations, but you'd lose the nice tabular overview and it's less consistent
    # with other example scripts
    keyword_adgroups["Keywords"] = True
    adgroups = all_adgroups.merge(keyword_adgroups, how="left")\
        .fillna(False)

    without_keywords = ~adgroups["Keywords"]
    return adgroups[without_keywords]


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    remove_empty_adgroups(adwords_credentials_path, is_debug=True)
