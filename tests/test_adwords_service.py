import pytest


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
        assert account.name == "Dont touch - !ImportantForTests!"

    for account in adwords_service.accounts(convert=False):
        # hack but I couldn't import the class. please fix if you can
        assert str(type(account)) == "<class 'suds.sudsobject.ManagedCustomer'>"
        assert account.name == "Dont touch - !ImportantForTests!"


def test_report_definition():
    from tests import adwords_service
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
    r_def = adwords_service.report_definition(r_type, fields, predicates)
    expected_result = {
        "reportName": "name",
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
    assert r_def == expected_result

    # conversion of date strings
    r_def2 = adwords_service.report_definition(
        report_type=r_type, fields=fields, date_min=seven_d_ago, date_max=yesterday)
    expected_result2 = {
        "reportName": "name",
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
    assert r_def2 == expected_result2

    # multiple specifications for date range
    with pytest.raises(IOError):
        adwords_service.report_definition(
            report_type=r_type, fields=fields, predicates=predicates,
            last_days=3, date_min=seven_d_ago, date_max=yesterday)


def test_download_report():
    import pandas as pd
    from tests import adwords_service

    # impression keywords (empty df since test account can't be served)
    r_def = adwords_service.report_definition(
        report_type="KEYWORDS_PERFORMANCE_REPORT", fields=["Criteria"])
    report = adwords_service.download_report(r_def)
    imp_result = pd.DataFrame(columns=["Criteria"])
    assert report.equals(imp_result)

    # zero impressions
    report = adwords_service.download_report(r_def, include_0_imp=True)
    zero_imp_result = pd.DataFrame([["test_kw_1"]], columns=["Criteria"])
    assert report.equals(zero_imp_result)


def test_download_objects():
    from tests import adwords_service

    fields = ["Id", "Criteria"]
    predicates = [{"field": "Criteria", "operator": "EQUALS", "values": "test_kw_1"}]
    result = adwords_service.download_objects(
        "AdGroupCriterionService", fields=fields, predicates=predicates)
    assert isinstance(result, list)
    assert len(result) == 1
    # hack but I couldn't import the class. please fix if you can
    assert str(type(result[0])) == "<class 'suds.sudsobject.BiddableAdGroupCriterion'>"
    assert result[0]["criterion"]["text"] == "test_kw_1"


def test_upload():
    pass
