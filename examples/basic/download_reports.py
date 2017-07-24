import freedan


credentials_path = "adwords_credentials.yaml"
adwords_service = freedan.AdWordsService(credentials_path)

fields = [
    "AdGroupId", "Id", "Criteria", "KeywordMatchType", "CpcBid",
    "Impressions", "Clicks", "Conversions", "Cost"
]
predicates = [{
    "field": "CampaignName",
    "operator": "DOES_NOT_CONTAIN_IGNORE_CASE",
    "values": "test"
}]

report_def = adwords_service.report_definition(
    report_type="KEYWORDS_PERFORMANCE_REPORT",
    fields=fields,
    predicates=predicates,
    last_days=7
)

for account in adwords_service.accounts():
    print(account)

    report = adwords_service.download_report(report_def, include_0_imp=True)
    print(report)
