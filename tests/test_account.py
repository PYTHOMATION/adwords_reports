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