import pytest


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