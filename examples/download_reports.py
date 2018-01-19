from py_adwords_reports import AdWordsClient, ReportDefinition


def download_reports(credentials, report_definition):
    """
    This script demonstrates the easy interface of accessing reports per account.
    :param credentials: str, path to your adwords credentials file
    :param report_definition: ReportDefinition
    """
    # init connection to adwords API
    adwords_service = AdWordsClient(credentials)

    # before the method is returning an account it 'selects' it,
    # i.e. it creates a new session with the scope of this account.
    # there's no other way to download reports in AdWords.
    for account in adwords_service.accounts():
        print(account)

        report = adwords_service.download_report(report_definition, zero_impressions=True)
        print(report)  # pandas DataFrame

        # you may now
        #   - stack reports of all your accounts
        #   - or save them to a csv
        #   - or push them to a database
        #   - ...


if __name__ == "__main__":
    credentials_path = "googleads.yaml"

    report_def = ReportDefinition(
        report_type="KEYWORDS_PERFORMANCE_REPORT",
        fields=[
            "AdGroupId", "Id", "Criteria", "KeywordMatchType", "CpcBid",
            "Impressions", "Clicks", "Conversions", "Cost"
        ],
        predicates=[{
            "field": "CampaignName",
            "operator": "DOES_NOT_CONTAIN_IGNORE_CASE",
            "values": "test"
        }],
        last_days=7
    )
    download_reports(credentials_path, report_def)
