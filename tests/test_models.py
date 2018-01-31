import pytest

from tests import init_native_adwords_account_label, init_native_adwords_account


def test_account_label():
    from adwords_reports.account import AccountLabel

    adwords_label = init_native_adwords_account_label("test_acc_label", 90)
    acc_label = AccountLabel.from_ad_account_label(adwords_label)
    assert acc_label.name == "test_acc_label"
    assert acc_label.id == 90


def test_account():
    from adwords_reports.account import Account, AccountLabel

    # test initiation from native adwords account
    adwords_account = init_native_adwords_account()
    account = Account.from_ad_account(ad_account=adwords_account)
    assert account.name == "Test1"
    assert account.id == "302-203-1203"
    assert account.currency == "CAD"
    assert account.time_zone == "America/Vancouver"

    # check labels
    assert all(isinstance(e, AccountLabel) for e in account.labels)
    label1, label2 = account.labels
    assert (label1.name, label1.id) == ("test1", 0)
    assert (label2.name, label2.id) == ("this_is_a_label", 1)


def test_micro_conversions():
    import adwords_reports.micro_amounts as micro_amounts

    assert micro_amounts.micro_to_reg(23000000) == 23.0
    assert micro_amounts.micro_to_reg(1111111) == 1.11
    assert micro_amounts.micro_to_reg(100) == 0.0

    assert micro_amounts.reg_to_micro(1.11) == 1110000
    assert micro_amounts.reg_to_micro(1.1111) == 1110000
    assert micro_amounts.reg_to_micro(0.003) == 0


def test_init_service():
    import googleads
    from tests import test_client

    account_service = test_client._init_service("ManagedCustomerService")
    assert isinstance(account_service, googleads.common.SudsServiceProxy)


def test_init_report_downloader():
    import googleads
    from tests import test_client

    report_downloader = test_client._init_report_downloader()
    assert isinstance(report_downloader, googleads.adwords.ReportDownloader)


def test_get_page():
    from tests import test_client
    from adwords_reports.account import ACCOUNT_SELECTOR

    result = test_client._get_page(ACCOUNT_SELECTOR, "ManagedCustomerService")
    # hack but I couldn't import the class. please fix if you can
    assert str(type(result)) == "<class 'suds.sudsobject.ManagedCustomerPage'>"


def test_account_iterator():
    from adwords_reports.account import Account
    from tests import test_client

    for account in test_client.accounts():
        assert isinstance(account, Account)
        assert account.name == "Dont touch - !ImportantForTests!"


def test_report_definition():
    from adwords_reports.report_definition import ReportDefinition
    import datetime

    today = datetime.date.today()
    yesterday = (today - datetime.timedelta(1)).strftime("%Y-%m-%d")
    seven_d_ago = (today - datetime.timedelta(7)).strftime("%Y-%m-%d")
    yesterday_clean = yesterday.replace("-", "")
    seven_d_ago_clean = seven_d_ago.replace("-", "")

    r_type = "KEYWORDS_PERFORMANCE_REPORT"
    fields = ["Criteria"]
    predicates = [{"field": "Name", "operator": "EQUALS", "values": "test_kw_1"}]
    # check if structure is as intended
    r_def = ReportDefinition(r_type, fields, predicates, last_days=7)
    expected_result = {
        "reportName": "api_report",
        "dateRangeType": "CUSTOM_DATE",
        "reportType": r_type,
        "downloadFormat": "CSV",
        "selector": {
            "fields": fields,
            "dateRange": {
                "min": seven_d_ago_clean,
                "max": yesterday_clean
            },
            "predicates": predicates
        }
    }
    assert r_def._as_dict() == expected_result

    # conversion of date strings
    r_def2 = ReportDefinition(
        report_type=r_type, fields=fields, date_from=seven_d_ago, date_to=yesterday)
    expected_result2 = {
        "reportName": "api_report",
        "dateRangeType": "CUSTOM_DATE",
        "reportType": r_type,
        "downloadFormat": "CSV",
        "selector": {
            "fields": fields,
            "dateRange": {
                "min": seven_d_ago_clean,
                "max": yesterday_clean
            }
        }
    }
    assert r_def2._as_dict() == expected_result2

    # multiple specifications for date range
    with pytest.raises(AssertionError):
        ReportDefinition(
            report_type=r_type, fields=fields, predicates=predicates,
            last_days=3, date_from=seven_d_ago, date_to=yesterday)


def test_download_report():
    import pandas as pd
    from tests import test_client
    from adwords_reports.report_definition import ReportDefinition

    # impression keywords (empty df since test account can't be served)
    r_def = ReportDefinition(
        report_type="KEYWORDS_PERFORMANCE_REPORT", fields=["Criteria"], last_days=7)
    report = test_client._download_report(r_def, zero_impressions=False)
    imp_result = pd.DataFrame(columns=["Criteria"])
    assert report.equals(imp_result)

    # zero impressions
    report = test_client._download_report(r_def, zero_impressions=True)
    zero_imp_result = pd.DataFrame([["test_kw_1"]], columns=["Criteria"])
    assert report.equals(zero_imp_result)
