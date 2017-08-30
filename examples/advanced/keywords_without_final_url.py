import freedan


def keywords_without_final_url(path_credentials):
    """
    A script that finds all keywords without a final url

    Most of the time it's better to set up your final url on keyword level rather than on ad level, because keywords
    represent the user intend better.
    :param path_credentials: str, path to your adwords credentials file
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        keywords = identify_keywords_without_final_url(adwords_service)
        if keywords.empty:
            continue

        print(keywords)

        # add your custom logic to create according final urls here
        # ...


def identify_keywords_without_final_url(adwords_service):
    """ Download all keywords and identify the ones with missing pluses
    :param adwords_service: AdWordsService object
    :return: DataFrame
    """
    fields = [
        "AdGroupName", "AdGroupId", "Criteria", "Id",
        "KeywordMatchType", "Status", "FinalUrls"
    ]
    predicates = [{
        "field": "FinalUrls",
        "operator": "DOES_NOT_CONTAIN",
        "values": "http"
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

    keywords_report_def = adwords_service.report_definition("KEYWORDS_PERFORMANCE_REPORT", fields, predicates)
    urlless_keywords = adwords_service.download_report(keywords_report_def, include_0_imp=True)
    return urlless_keywords


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    keywords_without_final_url(adwords_credentials_path)
