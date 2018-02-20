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