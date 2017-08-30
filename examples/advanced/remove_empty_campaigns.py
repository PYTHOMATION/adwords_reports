import freedan
from freedan import Campaign


def remove_empty_campaigns(path_credentials, is_debug):
    """
    A script that will delete all empty Campaigns in all accounts.
    A Campaign is considered to be empty if it doesn't contain any AdGroups.

    :param path_credentials: str, path to your adwords credentials file
    :param is_debug: bool
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        empty_campaigns = identify_empty_campaigns(adwords_service)
        # potentially save this DataFrame as a changelog

        operations = build_operations(empty_campaigns)
        adwords_service.upload(operations, is_debug=is_debug)


def build_operations(adgroups):
    """ Build delete operations for Campaigns
    :param adgroups: DataFrame
    :return: list of operations
    """
    operations = list()
    for index, row in adgroups.iterrows():
        campaign_id = int(row["CampaignId"])
        delete_operation = Campaign.delete_operation(campaign_id=campaign_id)
        operations.append(delete_operation)
    return operations


def identify_empty_campaigns(adwords_service):
    """ Download all Campaigns and identify which don't have AdGroups
    :param adwords_service: AdWordsService object
    :return: DataFrame
    """
    # ignore deleted entities
    fields = ["CampaignName", "CampaignId"]
    predicates = [{
        "field": "CampaignStatus",
        "operator": "NOT_EQUALS",
        "values": "REMOVED"
    }]

    # the adgroup report will contain all adgroups of the account
    campaign_report_def = adwords_service.report_definition("CAMPAIGN_PERFORMANCE_REPORT", fields, predicates)
    all_campaigns = adwords_service.download_report(campaign_report_def, include_0_imp=True)
    if all_campaigns.empty:  # skip rest if no campaigns in the account. otherwise merge below triggers warning
        return all_campaigns

    # the keyword report will only contain adgroups belonging to keywords in the account
    adgroup_report_def = adwords_service.report_definition("ADGROUP_PERFORMANCE_REPORT", fields, predicates)
    adgroup_campaigns = adwords_service.download_report(adgroup_report_def, include_0_imp=True)

    # identify all adgroups in adgroup_report that are not in keyword_report
    # could also be done with set operations, but you'd lose the nice tabular overview and it's less consistent
    # with other example scripts
    adgroup_campaigns["has_adgroups"] = True
    campaigns = all_campaigns.merge(adgroup_campaigns, how="left")\
        .fillna(False)

    without_adgroups = ~campaigns["has_adgroups"]
    return campaigns[without_adgroups]


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    remove_empty_campaigns(adwords_credentials_path, is_debug=True)
