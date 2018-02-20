import pandas as pd

from tests import (fix_client, fix_account, fix_report_definition, fix_account_label,
                   fix_adwords_account_service, fix_adwords_account_label, fix_adwords_account)  # is used


def test_account_selector():
    from adwords_reports.account import Account

    assert Account.SELECTOR == {
        "fields": ["Name", "CustomerId", "CurrencyCode", "DateTimeZone"],
        "predicates": [{
            "field": "CanManageClients",
            "operator": "EQUALS",
            "values": "FALSE"
        }],
        "ordering": [{
            "field": "Name",
            "sortOrder": "ASCENDING"
        }]
    }


def test_init(fix_client):
    from adwords_reports.account import Account

    assert Account(
        client=fix_client,
        account_id="519-085-5164",
        name="Dont touch - !ImportantForTests!",
        currency="CAD",
        time_zone="America/Vancouver",
        labels=list()
    )


def test_from_ad_account(fix_client, fix_adwords_account):
    from adwords_reports.account import Account
    from adwords_reports.account_label import AccountLabel

    # test initiation from native adwords account
    account = Account.from_ad_account(fix_client, fix_adwords_account)
    assert account.name == "Test1"
    assert account.id == "519-085-5164"
    assert account.currency == "CAD"
    assert account.time_zone == "America/Vancouver"
    assert isinstance(account.labels, list)
    assert isinstance(account.labels[0], AccountLabel)


def test_download_report_impressions(fix_account, fix_report_definition):
    # impression keywords (empty df since test account can't be served)

    report = fix_account.download(fix_report_definition, zero_impressions=False)
    expected_result = pd.DataFrame(columns=["Criteria"])
    assert report.equals(expected_result)


def test_download_report_zero_impressions(fix_account, fix_report_definition):
    report = fix_account.download(fix_report_definition, zero_impressions=True)
    expected_result = pd.DataFrame([["test_kw_1"]], columns=["Criteria"])
    assert report.equals(expected_result)


def test_repr(fix_account):
    assert str(fix_account) == "\nAccountName: Dont touch - !ImportantForTests! (ID: 5190855164)"
