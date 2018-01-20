import io
import datetime
import pandas as pd

from adwords_reports.error_retryer import ErrorRetryer


@ErrorRetryer()
def download_report(downloader, report_definition, zero_impressions=False):
    """ Downloads a report to a temp csv -> dataframe
    :param downloader: adwords reportDownloader service
    :param report_definition: nested dict, refer to method "report_definition" for easy creation
    :param zero_impressions: bool
    :return: report as dataframe
    """
    report_definition = assert_dict(report_definition)
    header = report_definition["selector"]["fields"]

    data = downloader.DownloadReportAsString(
        report_definition, skip_report_header=True, skip_column_header=True,
        skip_report_summary=True, include_zero_impressions=zero_impressions)
    data = io.StringIO(data)
    return pd.read_csv(data, names=header)


def assert_dict(report_definition):
    if isinstance(report_definition, ReportDefinition):
        report_definition = report_definition.as_dict()
    assert isinstance(report_definition, dict)
    return report_definition


class ReportDefinition:
    def __init__(self, report_type, fields, predicates=None, last_days=None, date_min=None, date_max=None):
        """ Create report definition as needed in api call from meta information
        :param report_type: str, https://developers.google.com/adwords/api/docs/appendix/reports
        :param fields: list of str
        :param predicates: list of dicts
        :param last_days: int, date_max = yesterday and date_min = today - days_ago
                              not compatible with date_min/date_max
        :param date_min: str, format YYYYMMDD or YYYY-MM-DD
        :param date_max: str, format YYYYMMDD or YYYY-MM-DD
        """
        self.report_type = self.clean_report_type(report_type)
        self.fields = fields
        self.predicates = predicates

        self.date_min = date_min
        self.date_max = date_max
        self.determine_dates(last_days)

    @staticmethod
    def clean_report_type(report_type):
        return report_type\
            .upper()\
            .replace(" ", "_")

    def determine_dates(self, last_days):
        self.validate_inputs(last_days)

        if last_days is not None:
            self.calculate_dates_from_relative(last_days)
        self.standardize_date_format()

    def validate_inputs(self, last_days):
        dates_are_relative = last_days is not None
        dates_are_absolute = (self.date_min is not None) or (self.date_max is not None)

        assert dates_are_relative or dates_are_absolute, "No time range specified."
        assert not (dates_are_relative and dates_are_absolute), "Either absolute dates or relative dates."

    def calculate_dates_from_relative(self, last_days):
        today = datetime.date.today()
        self.date_max = (today - datetime.timedelta(1)).isoformat()
        self.date_min = (today - datetime.timedelta(last_days)).isoformat()

    def standardize_date_format(self):
        self.date_min = self.date_min.replace("-", "")
        self.date_max = self.date_max.replace("-", "")

    def as_dict(self):
        report_def = {
            "reportName": "api_report",
            "dateRangeType": "CUSTOM_DATE",
            "reportType": self.report_type,
            "downloadFormat": "CSV",
            "selector": {
                "fields": self.fields,
                "dateRange": {
                    "min": self.date_min,
                    "max": self.date_max
                }
            }
        }
        if self.predicates is not None:
            report_def["selector"]["predicates"] = self.predicates
        return report_def
