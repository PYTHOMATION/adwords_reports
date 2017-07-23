def test_micro_euro_conversion():
    from freedan import AdWordsService

    assert AdWordsService.micro_to_euro(23000000) == 23.0
    assert AdWordsService.micro_to_euro(1111111) == 1.11
    assert AdWordsService.micro_to_euro(100) == 0.0

    assert AdWordsService.euro_to_micro(1.11) == 1110000
    assert AdWordsService.euro_to_micro(1.1111) == 1110000
    assert AdWordsService.euro_to_micro(0.003) == 0


def test_init_service():
    import googleads
    from tests import adwords_service

    account_service = adwords_service.init_service("ManagedCustomerService")
    assert isinstance(account_service, googleads.common.SudsServiceProxy)

    report_downloader = adwords_service.init_service("ReportDownloader")
    assert isinstance(report_downloader, googleads.adwords.ReportDownloader)


def test_account_selector():
    from tests import adwords_service

    default_fields = [
        "Name", "CustomerId", "AccountLabels", "CanManageClients",
        "CurrencyCode", "DateTimeZone", "TestAccount"
    ]

    no_pred_mcc = adwords_service._account_selector(predicates=None, skip_mccs=False)
    assert no_pred_mcc == {
        "fields": default_fields,
        "ordering": [{
            "field": "Name",
            "sortOrder": "ASCENDING"
        }]
    }

    no_pred_no_mcc = adwords_service._account_selector(predicates=None, skip_mccs=True)
    assert no_pred_no_mcc == {
        "fields": default_fields,
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

    dummy_pred = [{"field": "Name", "operator": "EQUALS", "values": "Test1"}]
    pred_mcc = adwords_service._account_selector(predicates=dummy_pred, skip_mccs=False)
    assert pred_mcc == {
        "fields": default_fields,
        "predicates": [{
            "field": "Name",
            "operator": "EQUALS",
            "values": "Test1"
        }],
        "ordering": [{
            "field": "Name",
            "sortOrder": "ASCENDING"
        }]
    }

    pred_no_mcc = adwords_service._account_selector(predicates=dummy_pred, skip_mccs=True)
    assert pred_no_mcc == {
        "fields": default_fields,
        "predicates": [{
            "field": "Name",
            "operator": "EQUALS",
            "values": "Test1"
        }, {
            "field": "CanManageClients",
            "operator": "EQUALS",
            "values": "FALSE"
        }],
        "ordering": [{
            "field": "Name",
            "sortOrder": "ASCENDING"
        }]
    }


def test_get_page():
    from tests import adwords_service

    acc_selector = adwords_service._account_selector(predicates=None, skip_mccs=True)
    result = adwords_service._get_page(acc_selector, "ManagedCustomerService")
    # hack but I couldn't import the class. please fix if you can
    assert str(type(result)) == "<class 'suds.sudsobject.ManagedCustomerPage'>"


def test_account_iterator():
    from freedan import Account
    from tests import adwords_service

    for account in adwords_service.accounts(convert=True):
        assert isinstance(account, Account)
        assert account.name == "Dont touch - !ImportantAccountForTests!"

    for account in adwords_service.accounts(convert=False):
        # hack but I couldn't import the class. please fix if you can
        assert str(type(account)) == "<class 'suds.sudsobject.ManagedCustomer'>"
        assert account.name == "Dont touch - !ImportantAccountForTests!"
