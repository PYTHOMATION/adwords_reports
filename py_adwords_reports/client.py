from googleads import adwords

from py_adwords_reports import base_dir
from py_adwords_reports.error_retryer import ErrorRetryer

import py_adwords_reports.handler_reports as handler_reports
import py_adwords_reports.handler_accounts as handler_accounts


DEFAULT_CREDENTIALS_PATH = base_dir+"/googleads.yaml"
DEFAULT_API_VERSION = "v201710"
MICRO_FACTOR = 10**6


class AdWordsClient:
    """ AdWords service class that handles interactions with AdWords API and provides a top-level interface for this api.
    Most important functionality:
        - Initiate API connection using credentials
        - Generator for accounts matching the account selector in project _config
        - Download reports
    """
    def __init__(self, credentials_path=DEFAULT_CREDENTIALS_PATH, api_version=DEFAULT_API_VERSION):
        self._client = self._init_api_connection(credentials_path)
        self.top_level_account_id = self._client.client_customer_id
        self.api_version = api_version

    def download_report(self, report_definition, zero_impressions):
        """
        :param report_definition: ReportDefinition or nested dict
        :param zero_impressions: bool
        :return: DataFrame
        """
        downloader = self._init_report_downloader()
        report = handler_reports.download_report(
            downloader=downloader,
            report_definition=report_definition,
            zero_impressions=zero_impressions)
        return report

    def accounts(self):
        """
        :return: generator with Account objects sorted by name
        """
        account_selector = handler_accounts.ACCOUNT_SELECTOR
        ad_accounts = self._get_entries(account_selector, service="ManagedCustomerService")

        for ad_account in ad_accounts:
            account = handler_accounts.Account.from_ad_account(ad_account=ad_account)
            self.select(account)
            yield account
        self.reset_selection()

    def select(self, account_or_id):
        """ starts a new session with the scope of this account.
        :param account_or_id: int/float or Account
        """
        account_id = handler_accounts.to_account_id(account_or_id)
        self._client.SetClientCustomerId(account_id)

    def reset_selection(self):
        """ resets scope to the top level account/mcc used in the .yaml file """
        self.select(self.top_level_account_id)

    def _get_entries(self, selector, service):
        """
        :param selector: nested dict that describes what is requested
        :param service: str, identifying adwords service that is responsible
        :return: adwords page object
        """
        page = self._get_page(selector, service)
        if "entries" not in page:
            raise LookupError("Nothing matches the selector.")
        return page["entries"]

    @ErrorRetryer()
    def _get_page(self, selector, service):
        """
        :param selector: nested dict that describes what is requested
        :param service: str, identifying adwords service that is responsible
        :return: adwords page object
        """
        service_object = self._init_service(service)
        return service_object.get(selector)

    @ErrorRetryer()
    def _init_service(self, service_name):
        return self._client.GetService(service_name, version=self.api_version)

    @ErrorRetryer()
    def _init_report_downloader(self):
        return self._client.GetReportDownloader(version=self.api_version)

    @ErrorRetryer()
    def _init_api_connection(self, credentials_path):
        return adwords.AdWordsClient.LoadFromStorage(credentials_path)
