import io
import time
import datetime
import pandas as pd
from googleads import adwords

from freedan.adwords_objects.account import Account
from freedan.adwords_services.standard_uploader import StandardUploader
from freedan.adwords_services.batch_uploader import BatchUploader
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


class AdWordsService:
    """ AdWords Service class that handles interactions with AdWords API. Most important functionality:
        - Initiate API connection using credentials
        - Generator for accounts matching the account selector in project _config
        - Download reports
        - Upload operations using standard or batch functionality
    """
    def __init__(self, credentials_path, api_version=DEFAULT_API_VERSION):
        """
        :param api_version: str, normally you want to use the most recent version
        :param credentials_path: str, path to .yaml file
        """
        self.credentials_path = credentials_path
        self.api_version = api_version
        self.client = self._init_api_connection()
        self.top_level_account_id = self.client.client_customer_id
        self.report_downloader = self.init_service("ReportDownloader")

    @staticmethod
    def euro_to_micro(number):
        """ Convert a number to an micro amount:
            - times one million
            - and rounded to multiples of 10k """
        assert isinstance(number, (float, int))
        return int(round(float(number) * MICRO_FACTOR, -4))

    @staticmethod
    def micro_to_euro(number):
        """ Convert micro amount to regular euro amount
            - divided by one million
            - and rounded to 2 fractional digits """
        assert isinstance(number, int)
        return round(float(number) / MICRO_FACTOR, 2)

    @ErrorRetryer()
    def _init_api_connection(self):
        """ Initiates the adwords api client object """
        return adwords.AdWordsClient.LoadFromStorage(self.credentials_path)

    @ErrorRetryer()
    def init_service(self, service_name):
        """ Initiates the adwords services or report downloader """
        if self.client is None:
            raise ConnectionError("Please initiate API connection first using .initiate_api_connection()")

        if service_name == "ReportDownloader":
            return self.client.GetReportDownloader(version=self.api_version)
        else:
            return self.client.GetService(service_name, version=self.api_version)

    @ErrorRetryer()
    def _get_page(self, selector, service):
        """ Get "page" object of adwords objects (an iterable containing adwords objects)
        :param selector: nested dict that describes what is requested
        :param service: str, identifying adwords service that is responsible
        :return: adwords page object
        """
        service_object = self.init_service(service)
        return service_object.get(selector)

    def accounts(self, predicates=None, skip_mccs=True, convert=True):
        """ Generator yielding accounts + business info ordered by account name
        :param predicates:
        :param skip_mccs:
        :param convert: bool, convert to SearchAccount object
        :return: generator yielding dicts with core information of accounts
        """
        account_selector = self._account_selector(predicates, skip_mccs)
        account_page = self._get_page(account_selector, "ManagedCustomerService")
        if "entries" not in account_page:
            raise LookupError("Nothing matches the selector.")

        for ad_account in account_page["entries"]:
            self.client.SetClientCustomerId(ad_account.customerId)  # select account

            if convert:
                yield Account.from_ad_account(ad_account=ad_account)
            else:
                yield ad_account

    @staticmethod
    def _account_selector(predicates, skip_mccs):
        account_selector = {
            "fields": [
                "Name", "CustomerId", "AccountLabels", "CanManageClients",
                "CurrencyCode", "DateTimeZone", "TestAccount"
            ],
            "ordering": [{
                "field": "Name",
                "sortOrder": "ASCENDING"
            }]
        }

        if predicates is not None:
            account_selector["predicates"] = predicates

        if skip_mccs:
            skip_mcc_predicate = {
                "field": "CanManageClients",
                "operator": "EQUALS",
                "values": "FALSE"
            }
            if "predicates" in account_selector:
                account_selector["predicates"].append(skip_mcc_predicate)
            else:
                account_selector["predicates"] = [skip_mcc_predicate]
        return account_selector

    @staticmethod
    def report_definition(report_type, fields, predicates=None, last_days=None, date_min=None, date_max=None):
        """ Create report definition as needed in api call from meta information
        If date range isn't specified, last_days will be set to 7
        :param report_type: str, https://developers.google.com/adwords/api/docs/appendix/reports
        :param fields: list of str
        :param last_days: int, date_max = yesterday and date_min = today - days_ago
                              not compatible with date_min/date_max
        :param date_min: str, format YYYYMMDD or YYYY-MM-DD
                              not compatible with date_min/date_max
        :param date_max: str, format YYYYMMDD or YYYY-MM-DD
                              not compatible with date_min/date_max
        :param predicates: list of dicts
        """
        dates_are_relative = last_days is not None
        dates_are_absolute = date_min is not None or date_max is not None
        if dates_are_absolute:
            assert date_min and date_max

        # validate input parameters
        if dates_are_relative and dates_are_absolute:
            raise IOError("Please choose either days_ago or date_min/date_max for date range specification.")
        elif not dates_are_relative and not dates_are_absolute:
            last_days = 7
            dates_are_relative = True

        # compute dates
        if dates_are_relative:
            today = datetime.date.today()
            date_max = (today - datetime.timedelta(1)).strftime("%Y%m%d")
            date_min = (today - datetime.timedelta(last_days)).strftime("%Y%m%d")

        # standardize report type
        report_type = report_type.upper() \
            .replace(" ", "_")

        report_def = {
            "reportName": "name",
            "dateRangeType": "CUSTOM_DATE",
            "reportType": report_type,
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

    @ErrorRetryer()
    def download_report(self, report_definition, include_0_imp=False):
        """ Downloads a report to a temp csv -> dataframe
        :param report_definition: nested dict, refer to method "report_definition" for easy creation
        :param include_0_imp: bool
        :return: report as dataframe
        """
        header = report_definition["selector"]["fields"]
        data = self.report_downloader.DownloadReportAsString(
            report_definition, skip_report_header=True, skip_column_header=True,
            skip_report_summary=True, include_zero_impressions=include_0_imp)
        data = io.StringIO(data)
        report = pd.read_csv(data, names=header)
        return report

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

    def upload(self, operations, is_debug, partial_failure=True, service_name=None, is_label=False, method="standard",
               report_on_results=True, batch_sleep_interval=-1):
        """ Taking care of all scenarios when operations need to be uploaded to AdWords.
        :param operations: list of operations
        :param is_debug: bool
        :param partial_failure: bool
        :param service_name: service of operations. not needed for batch upload
        :param is_label: bool. Label upload works slightly different
        :param method: method for uploads < 5k. standard is faster, but less powerful
        :param report_on_results: bool, whether batchjob should download results or not
        :param batch_sleep_interval: int, -1 = exponential
        :return:
        """
        assert isinstance(operations, (list, tuple))
        if method == "batch" and isinstance(operations, list):
            operations = (operations, )

        amount_operations = sum(len(part) if isinstance(part, list) else 1 for part in operations)
        print("\nAmount of operations:", amount_operations)

        if amount_operations == 0:
            return None

        elif method == "standard":
            standard_uploader = StandardUploader(self, is_debug, partial_failure)
            return standard_uploader.execute(operations, service_name, is_label)

        elif method == "batch":
            return self.__batch_upload(operations, is_debug, report_on_results, batch_sleep_interval)
        else:
            raise IOError("method must be 'standard' or 'batch'.")

    def __batch_upload(self, operations, is_debug, report_on_results, batch_sleep_interval):
        """ Uploads a batch of operations to adwords api using batch job service.
        :param operations: tuple of lists of operations
        :param report_on_results: bool, specifies whether one should download results or not. Skipping speeds up execution
        :param batch_sleep_interval: int, sleeping time between checks on results. -1: using exponential time
        :return: return value of adwords
        """
        print("Uploading operations using batchjob")
        print("##### OperationUpload is LIVE: {is_live}. #####".format(is_live=(not is_debug)))
        if is_debug:
            print("Operations not uploaded due to debug. BatchUpload doesn't support validate only header...")
            return None

        else:
            batch_uploader = BatchUploader(self)
            batch_uploader.upload_operation(operations)

            # report on partial failures
            if report_on_results:
                return batch_uploader.report_on_results(batch_sleep_interval)
            else:
                return None

    @ErrorRetryer()
    def batch_job_helper(self):
        """ Get an AdWords BatchJobHelper object
        E.g. for temporary ids """
        return self.client.GetBatchJobHelper(version=self.api_version)
