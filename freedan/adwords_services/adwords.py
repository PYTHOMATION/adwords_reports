import os
import time
import uuid

import datetime
import pandas as pd
from googleads import adwords

from freedan.adwords_objects.account import Account
from freedan.adwords_services.adwords_standard_uploader import AdWordsStandardUploader
from freedan.adwords_services.adwords_batch_uploader import AdWordsBatchUploader
from freedan.other_services.error_retryer import ErrorRetryer

DEFAULT_API_VERSION = "v201705"

# max and min bid modifiers
MAX_BID_MODIFIER = 10.0
MIN_BID_MODIFIER = 0.1

MICRO_FACTOR = 1000000  # one million. AdWords uses micro amounts internally
DEVICE_TO_ID = {  # Internal ids of AdWords for different platforms
    "computers": 30000,
    "mobile": 30001,
    "tablet": 30002
}
PAGE_SIZE = 5000  # Recommended paging size by AdWords


class AdWords:
    """ AdWords Service class that handles interactions with AdWords API. Most important functionality:
        - Initiate API connection using credentials
        - Generator for accounts matching the account selector in project _config
        - Download reports
        - Upload operations using standard or batch functionality
    """
    def __init__(self, credentials_path, api_version=DEFAULT_API_VERSION, report_path=None):
        """
        :param api_version: str, normally you want to use the most recent version
        :param credentials_path: str, path to .yaml file
        :param report_path: default path used in download_report method
        """
        self.api_version = api_version
        self.credentials_path = credentials_path
        self.report_path = report_path
        self.client = self._init_api_connection()
        self.report_downloader = self._init_service("ReportDownloader")

    @staticmethod
    def euro_to_micro(number):
        """ Convert a number to an micro amount:
            - times one million
            - and rounded to multiples of 10k """
        return int(round(float(number) * MICRO_FACTOR, -4))

    @staticmethod
    def micro_to_euro(number):
        """ Convert micro amount to regular euro amount
            - divided by one million
            - and rounded to 2 fractional digits """
        return round(float(number) / MICRO_FACTOR, 2)

    @ErrorRetryer()
    def _init_api_connection(self):
        """ Initiates the adwords api client object """
        return adwords.AdWordsClient.LoadFromStorage(self.credentials_path)

    @ErrorRetryer()
    def _init_service(self, service_string):
        """ Initiates the adwords services or report downloader """
        if self.client is None:
            raise ConnectionError("Please initiate API connection first using .initiate_api_connection()")

        if service_string == "ReportDownloader":
            return self.client.GetReportDownloader(version=self.api_version)
        else:
            return self.client.GetService(service_string, version=self.api_version)

    @ErrorRetryer()
    def _get_page(self, selector, service):
        """ Get "page" object of adwords objects (an iterable containing adwords objects)
        :param selector: nested dict that describes what is requested
        :param service: str, identifying adwords service that is responsible
        :return: adwords page object
        """
        service_object = self._init_service(service)
        return service_object.get(selector)

    def accounts(self, fields=("Name", "CustomerId", "AccountLabels"), predicates=None, convert=True):
        """ Generator yielding accounts + business info ordered by account name
        :param fields:
        :param predicates:
        :param convert: bool, convert to SearchAccount object
        :return: generator yielding dicts with core information of accounts
        """
        account_selector = {
            "fields": list(fields)
        }
        if predicates is not None:
            account_selector["predicates"] = predicates

        account_dict = self._accounts_by_name(account_selector)
        for account_name in sorted(account_dict.keys()):
            ad_account = account_dict[account_name]
            self.client.SetClientCustomerId(ad_account.customerId)  # select account

            if convert:
                yield Account.from_ad_account(ad_account=ad_account)
            else:
                yield ad_account

    def _accounts_by_name(self, account_selector):
        """ Creating dict with account_name -> SearchAccount """
        if self.client is None:
            raise ConnectionError("Please initiate API connection first")

        account_page = self._get_page(account_selector, "ManagedCustomerService")
        if 'entries' not in account_page:
            raise LookupError("Nothing matches the selector.")
        return {account["name"]: account for account in account_page['entries']}

    @ErrorRetryer()
    def download_report(self, report_definition, zero_impressions=False):
        """ Downloads a report to a temp csv -> dataframe
        :param report_definition: nested dict, refer to method "report_definition" for easy creation
        :param zero_impressions: bool
        :return: report as dataframe
        """
        file_name = "temp_{uid}.csv".format(uid=uuid.uuid4().int)
        report_path = os.path.join(self.report_path, file_name)
        with open(report_path, mode='w') as report_csv:
            header = report_definition["selector"]["fields"]
            report_csv.write(",".join(header) + "\n")
            self.report_downloader.DownloadReport(
                report_definition, report_csv, skip_report_header=True, skip_column_header=True,
                skip_report_summary=True, include_zero_impressions=zero_impressions)

        report = pd.read_csv(report_path, encoding="utf-8")
        os.remove(report_path)
        return report

    @staticmethod
    def report_definition(report_type, fields, days_ago, date_min, date_max, predicates):
        """ Create report definition as needed in api call from meta information
        :param report_type: str, https://developers.google.com/adwords/api/docs/appendix/reports
        :param fields: list of str
        :param days_ago: int, date_max = today and date_min = today-days_ago
                              not compatible with date_min/date_max
        :param date_min: str, format YYYYMMDD or YYYY-MM-DD
                              not compatible with date_min/date_max
        :param date_max: str, format YYYYMMDD or YYYY-MM-DD
                              not compatible with date_min/date_max
        :param predicates: list of dicts
        """
        dates_are_relative = days_ago is not None
        dates_are_absolute = date_min is not None or date_max is not None
        if dates_are_absolute:
            assert date_min and date_max

        # validate input parameters
        if dates_are_relative and dates_are_absolute:
            raise IOError("Please choose either days_ago or date_min/date_max for date range specification.")
        elif not (dates_are_relative or dates_are_absolute):
            raise IOError("Please specify a date range.")

        # compute dates
        if dates_are_relative:
            today = datetime.date.today()
            date_max = today.strftime("%Y%m%d")
            date_min = (today - datetime.timedelta(days_ago)).strftime("%Y%m%d")

        report_def = {
            "reportName": "name",
            "dateRangeType": "CUSTOM_DATE",
            "reportType": report_type.upper(),
            "downloadFormat": "CSV",
            "selector": {
                "fields": fields,
                "dateRange": {
                    "min": date_min.replace("-", ""),
                    "max": date_max.replace("-", "")
                }
            }
        }
        if predicates is not None:
            report_def["selector"]["predicates"] = predicates

        return report_def

    def download_objects(self, service, fields=("Id", ), predicates=None):
        """ Downloads adwords objects the classical way
        CAUTION: Only use this, when necessary i.e. if there's no report type available containing this information
        For instance campaign language targetings are a use case for that
        :param service: str, identifying adwords service that's associated with those objects
        :param fields: list of str
        :param predicates: list of dicts
        :return: list of objects
        """
        offset = 0
        more_pages = True
        request = {
            "fields": list(fields),
            "paging": {
                'startIndex': str(offset),
                'numberResults': str(PAGE_SIZE)
            }
        }
        if predicates is not None:
            request["request"] = predicates

        results = list()
        while more_pages:
            page = self._get_page(request, service)
            if 'entries' not in page:
                raise LookupError("Nothing matches the selector.")

            results += [obj for obj in page['entries']]

            offset += PAGE_SIZE
            request['paging']['startIndex'] = str(offset)
            more_pages = offset < int(page['totalNumEntries'])
            time.sleep(0.5)
        return results

    def upload(self, operations, debug, partial_failure=True, service_string=None, label=False, method="standard",
               report_on_results=True, batch_sleep_interval=-1):
        """ Taking care of all scenarios when operations need to be uploaded to AdWords.
        :param operations: list of operations
        :param debug: bool
        :param partial_failure: bool
        :param service_string: service of operations. not needed for batch upload
        :param label: bool. Label upload works slightly different
        :param method: method for uploads < 5k. standard is faster, but less powerful
        :param report_on_results: bool, whether batchjob should download results or not
        :param batch_sleep_interval: int, -1 = exponential
        :return:
        """
        assert method in ["standard", "batch"]
        assert isinstance(operations, (list, tuple))
        if method == "batch" and isinstance(operations, list):
            operations = (operations, )

        amount_operations = sum(len(part) if isinstance(part, list) else 1 for part in operations)
        print("\nAmount of operations:", amount_operations)

        if amount_operations == 0:
            return None
        elif method == "standard":
            return self.__standard_upload(service_string, operations, debug, partial_failure, label)
        else:
            return self.__batch_upload(operations, debug, report_on_results, batch_sleep_interval)

    def __standard_upload(self, service_string, operations, debug, partial_failure, label):
        """ Upload operations using the AdWords standard upload """
        if service_string is None:
            raise IOError("Please provide the according service of the operations")
        standard_upload = AdWordsStandardUploader(self)
        return standard_upload.upload(service_string, operations, debug, partial_failure, label)

    def __batch_upload(self, operations, debug, report_on_results, batch_sleep_interval):
        """ Uploads a batch of operations to adwords api using batch job service.
        :param operations: tuple of lists of operations
        :param report_on_results: bool, specifies whether one should download results or not. Skipping speeds up execution
        :param batch_sleep_interval: int, sleeping time between checks on results. -1: using exponential time
        :return: return value of adwords
        """
        print("Uploading operations using batchjob")
        print("##### OperationUpload is LIVE: {is_live}. #####".format(is_live=(not debug)))
        if debug:
            print("Operations not uploaded due to debug. BatchUpload doesn't support validate only header...")
            return None

        else:
            batch_job = AdWordsBatchUploader(self)
            batch_job.upload_operation(operations)

            # report on partial failures
            if report_on_results:
                return batch_job.report_on_results(batch_sleep_interval)
            else:
                return None

    @ErrorRetryer()
    def batch_job_helper(self):
        """ Get an AdWords BatchJobHelper object
        E.g. for temporary ids """
        return self.client.GetBatchJobHelper(version=self.api_version)
