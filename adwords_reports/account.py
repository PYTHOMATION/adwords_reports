import io
import pandas as pd
from retrying import retry

from adwords_reports import logger
from adwords_reports.account_label import AccountLabel


class Account:
    SELECTOR = {
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

    def __init__(self, client, account_id, name, currency, time_zone, labels):
        self.client = client
        self.id = account_id
        self.name = name
        self.currency = currency
        self.time_zone = time_zone
        self.labels = labels

    @classmethod
    def from_ad_account(cls, client, ad_account):
        labels = cls.parse_labels(ad_account)
        return cls(client=client, account_id=ad_account.customerId, name=ad_account.name,
                   currency=ad_account.currencyCode, time_zone=ad_account.dateTimeZone,
                   labels=labels)

    def download(self, report_definition, zero_impressions):
        """ Downloads a report from the API
        :param report_definition: ReportDefinition
        :param zero_impressions: bool
        :return: DataFrame
        """
        json_report_definition = report_definition.raw
        header = json_report_definition["selector"]["fields"]

        response = self._download(json_report_definition, zero_impressions)
        data = io.StringIO(response)
        return pd.read_csv(data, names=header)

    @retry(stop_max_attempt_number=3, wait_random_min=5000, wait_random_max=10000)
    def _download(self, json_report_definition, zero_impressions):
        logger.info("Downloading report.")
        downloader = self.client.downloader
        response = downloader.DownloadReportAsString(
            json_report_definition, skip_report_header=True, skip_column_header=True,
            skip_report_summary=True, include_zero_impressions=zero_impressions)
        return response

    @staticmethod
    def parse_labels(ad_account):
        if "accountLabels" in ad_account:
            return [AccountLabel.from_ad_account_label(ad_label)
                    for ad_label in ad_account["accountLabels"]]
        else:
            return list()

    def __repr__(self):
        return "\nAccountName: {name} (ID: {id})".format(name=self.name, id=self.id)
