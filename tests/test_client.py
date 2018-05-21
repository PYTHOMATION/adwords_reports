import os
import pytest

from adwords_reports.client import Client

from tests import test_dir
from tests import fix_client  # is used


def test_default_api_version():
    from adwords_reports.client import DEFAULT_API_VERSION
    assert DEFAULT_API_VERSION == "v201802"


def test_init():
    test_credentials = os.path.join(test_dir, "test_googleads.yaml")
    assert Client(test_credentials)


def test_init_service(fix_client):
    import googleads

    account_service = fix_client._init_service("ManagedCustomerService")
    assert isinstance(account_service, googleads.common.SudsServiceProxy)


def test_init_report_downloader(fix_client):
    import googleads

    report_downloader = fix_client._init_report_downloader()
    assert isinstance(report_downloader, googleads.adwords.ReportDownloader)


def test_get_entries_results(fix_client):
    selector = {
        "fields": ["Name", "CustomerId", "CurrencyCode", "DateTimeZone"]
    }
    result = fix_client._get_entries(selector, "ManagedCustomerService")
    assert result
    assert isinstance(result, list)


def test_get_entries_no_results(fix_client):
    selector = {
        "fields": ["Name", "CustomerId", "CurrencyCode", "DateTimeZone"],
        "predicates": [{
            "field": "Name",
            "operator": "EQUALS",
            "values": "i_do_not_exist"
        }]
    }
    with pytest.raises(LookupError):
        fix_client._get_entries(selector, "ManagedCustomerService")


def test_select(fix_client):
    assert fix_client._client.client_customer_id == "519-085-5164"
    fix_client.select("873-154-8394")
    assert fix_client._client.client_customer_id == "873-154-8394"


def test_reset_selection(fix_client):
    assert fix_client._client.client_customer_id == "519-085-5164"
    fix_client.select("873-154-8394")
    assert fix_client._client.client_customer_id == "873-154-8394"
    fix_client.reset_selection()
    assert fix_client._client.client_customer_id == "519-085-5164"


def test_account_iterator(fix_client):
    from adwords_reports.account import Account

    for account in fix_client.accounts():
        assert isinstance(account, Account)
        assert account.name == "Dont touch - !ImportantForTests!"
