import io
import pandas as pd

from adwords_reports.error_retryer import ErrorRetryer


def to_account_id(obj):
    assert isinstance(obj, (Account, str, int, float))

    if isinstance(obj, Account):
        return obj.id
    else:
        return obj


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

    @ErrorRetryer()
    def _download(self, json_report_definition, zero_impressions):
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
        return list()

    def __repr__(self):
        return "\nAccountName: {name} (ID: {id})".format(name=self.name, id=self.id)


class AccountLabel:
    def __init__(self, name, label_id):
        self.id = label_id
        self.name = name

    @classmethod
    def from_ad_account_label(cls, adwords_acc_label):
        return cls(name=adwords_acc_label.name, label_id=adwords_acc_label.id)

    def __repr__(self):
        return "{name} ({id})".format(name=self.name, id=self.id)
