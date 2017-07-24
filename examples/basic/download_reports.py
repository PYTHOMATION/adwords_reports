import freedan


def download_reports(credentials_path, report_type, fields, predicates):
    """
    This script demonstrates the easy interface of accessing reports per account.

    If you wish to change the accounts touched by the script you may pass an account selector to the
    adwords_service.accounts method.
    You can create an account selector with adwords_service.account_selector
    :param credentials_path: str, path to your adwords credentials file
    :param report_type: str, str, https://developers.google.com/adwords/api/docs/appendix/reports
    :param fields: list of str, columns of report
    :param predicates: list of dict, filter
    """
    # init connection to adwords API
    adwords_service = freedan.AdWordsService(credentials_path)

    report_def = adwords_service.report_definition(
        report_type=report_type,
        fields=fields,
        predicates=predicates,
        last_days=7
    )

    # loop over accounts and download
    for account in adwords_service.accounts():
        print(account)

        report = adwords_service.download_report(report_def, include_0_imp=True)
        print(report)  # pandas DataFrame

        # you may now
        #   - stack reports of all your accounts to one big DataFrame
        #   - or save them to a csv
        #   - or push them to a data base
        #   - or ...


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"

    r_type = "KEYWORDS_PERFORMANCE_REPORT"
    r_fields = [
        "AdGroupId", "Id", "Criteria", "KeywordMatchType", "CpcBid",
        "Impressions", "Clicks", "Conversions", "Cost"
    ]
    r_predicates = [{
        "field": "CampaignName",
        "operator": "DOES_NOT_CONTAIN_IGNORE_CASE",
        "values": "test"
    }]
    download_reports(adwords_credentials_path, r_type, r_fields, r_predicates)
