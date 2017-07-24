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

    no_pred_mcc = adwords_service.account_selector(predicates=None, skip_mccs=False)
    assert no_pred_mcc == {
        "fields": default_fields,
        "ordering": [{
            "field": "Name",
            "sortOrder": "ASCENDING"
        }]
    }

    no_pred_no_mcc = adwords_service.account_selector(predicates=None, skip_mccs=True)
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
    pred_mcc = adwords_service.account_selector(predicates=dummy_pred, skip_mccs=False)
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

    pred_no_mcc = adwords_service.account_selector(predicates=dummy_pred, skip_mccs=True)
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

    acc_selector = adwords_service.account_selector(predicates=None, skip_mccs=True)
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


def test_too_many_operations_in_standard_upload():
    from tests import adwords_service, adgroup1_name, adgroup1_id
    from freedan import AdGroup

    correct_operations = [AdGroup.set_name_operation(adgroup_id=adgroup1_id, new_name=adgroup1_name)]

    # too many operations for standard upload
    too_many_operations = correct_operations * 5001
    with pytest.raises(IOError):
        adwords_service.upload(too_many_operations, is_debug=True, method="standard")

def test_good_upload():
    from tests import adwords_service, adgroup1_name, adgroup1_id
    from freedan import AdGroup

    correct_operations = [AdGroup.set_name_operation(adgroup_id=adgroup1_id, new_name=adgroup1_name)]

    adwords_service.upload(correct_operations, is_debug=True, method="standard")
    adwords_service.upload(correct_operations, is_debug=True, method="batch")
    adwords_service.upload(correct_operations, is_debug=False, method="standard")
    adwords_service.upload(correct_operations, is_debug=False, method="batch",
                           report_on_results=False, batch_sleep_interval=2)


def test_flawed_upload():
    from tests import adwords_service, adgroup1_name, adgroup1_id
    from freedan import AdGroup

    flawed_operations = [AdGroup.set_name_operation(adgroup_id=adgroup1_id + 1, new_name=adgroup1_name)]

    adwords_service.upload(flawed_operations, is_debug=True, method="standard")
    adwords_service.upload(flawed_operations, is_debug=True, method="batch", report_on_results=True)
    adwords_service.upload(flawed_operations, is_debug=False, method="standard")


def test_different_operation_types_in_standard_upload():
    from tests import adwords_service, adgroup1_name, adgroup1_id
    from freedan import AdGroup, Label

    # this test scenario is particularly interesting since both use the AdGroupService for upload.
    # but they use mutate and mutateLabel in the actual mutate call
    # so an error must be raised
    ag_label = Label("ag_label_test")
    ag_label.update_id(adwords_service, is_debug=True)
    correct_operations = [
        AdGroup.set_name_operation(adgroup_id=adgroup1_id, new_name=adgroup1_name),
        ag_label.apply_on_adgroup_operation(adgroup_id=adgroup1_id)
    ]

    with pytest.raises(IOError):
        adwords_service.upload(correct_operations, is_debug=True, method="standard")


def test_label_upload():
    from tests import adwords_service, adgroup1_id
    from freedan import Label

    ag_label = Label("ag_label_test")
    ag_label.update_id(adwords_service, is_debug=True)
    label_operations = [ag_label.apply_on_adgroup_operation(adgroup_id=adgroup1_id)]

    adwords_service.upload(label_operations, is_debug=True, method="standard")
    adwords_service.upload(label_operations, is_debug=True, method="batch")


def test_fillna_with_temp_id():
    import numpy as np
    from tests import adwords_service
    from freedan import BatchUploader

    batch_uploader = BatchUploader(adwords_service, is_debug=True, report_on_results=True, batch_sleep_interval=-1)
    assert batch_uploader.fillna_with_temp_id(np.nan) == -1
    assert batch_uploader.fillna_with_temp_id(-1) == -1
    assert batch_uploader.fillna_with_temp_id(230) == 230
    assert batch_uploader.fillna_with_temp_id(np.nan) == -2
    assert batch_uploader.fillna_with_temp_id("asjd") == "asjd"


def test_report_helper():
    import numpy as np
    import pandas as pd
    from freedan.adwords_services.report_helper import convert_adwords_columns, replace_special_float

    # special float conversion
    nan_df = pd.DataFrame([[np.inf, np.nan],
                           [np.nan, -np.inf]], columns=list("ab"))
    nan_series = nan_df["a"]

    zero_df = pd.DataFrame([[0.0, 0.0],
                            [0.0, 0.0]], columns=list("ab"))
    zero_series = zero_df["a"]
    assert replace_special_float(nan_series).equals(zero_series)
    assert replace_special_float(nan_df).equals(zero_df)
    assert replace_special_float(np.nan) == 0.0

    # adwords columns conversion
    # input df
    cols = [
        "CpcBid", "Cost", "SearchRankLostImpressionShare", "KeywordMatchType", "Criteria",
        "AdGroupDesktopBidModifier", "AdGroupMobileBidModifier", "AdGroupTabletBidModifier",
        "CampaignDesktopBidModifier", "CampaignMobileBidModifier", "CampaignTabletBidModifier"
    ]
    input_values = [
        [1000000, 1320000, " --", "Exact", "Asd", " --", "30%", "-10%", " --", "30%", "-10%"],
        [1000000, 1320000, "30%", "Phrase", "+asd", " --", "30%", "-10%", " --", "30%", "-10%"],
        [1000000, 1320000, "> 90%", "Broad", "asd", " --", "30%", "-10%", " --", "30%", "-10%"]
    ]
    adwords_df = pd.DataFrame(input_values, columns=cols)

    # expected
    new_cols = [
        "AdGroupDesktop_OperationType", "AdGroupMobile_OperationType", "AdGroupTablet_OperationType",
        "CampaignDesktop_OperationType", "CampaignMobile_OperationType", "CampaignTablet_OperationType"
    ]
    expected_values = [
        [1.0, 1.32, -1.0, "EXACT", "asd", 1.0, 1.3, 0.9, 1.0, 1.3, 0.9, "ADD", "SET", "SET", "ADD", "SET", "SET"],
        [1.0, 1.32, 0.3, "PHRASE", "asd", 1.0, 1.3, 0.9, 1.0, 1.3, 0.9, "ADD", "SET", "SET", "ADD", "SET", "SET"],
        [1.0, 1.32, 0.9, "BROAD", "asd", 1.0, 1.3, 0.9, 1.0, 1.3, 0.9, "ADD", "SET", "SET", "ADD", "SET", "SET"]
    ]
    expected_df = pd.DataFrame(expected_values, columns=cols+new_cols)

    expected_values_with_pluses = [
        [1.0, 1.32, -1.0, "EXACT", "asd", 1.0, 1.3, 0.9, 1.0, 1.3, 0.9, "ADD", "SET", "SET", "ADD", "SET", "SET"],
        [1.0, 1.32, 0.3, "PHRASE", "+asd", 1.0, 1.3, 0.9, 1.0, 1.3, 0.9, "ADD", "SET", "SET", "ADD", "SET", "SET"],
        [1.0, 1.32, 0.9, "BROAD", "asd", 1.0, 1.3, 0.9, 1.0, 1.3, 0.9, "ADD", "SET", "SET", "ADD", "SET", "SET"]
    ]
    expected_df_with_pluses = pd.DataFrame(expected_values_with_pluses, columns=cols+new_cols)

    assert convert_adwords_columns(adwords_df.copy()).equals(expected_df)
    assert convert_adwords_columns(adwords_df.copy(), add_operation_type=False).equals(expected_df[cols])
    assert convert_adwords_columns(adwords_df.copy(), remove_pluses=False).equals(expected_df_with_pluses)
