from googleads import adwords

from adwords_reports import base_dir
from adwords_reports.error_retryer import ErrorRetryer
from adwords_reports.account import Account, to_account_id


DEFAULT_CREDENTIALS_PATH = base_dir+"/googleads.yaml"
DEFAULT_API_VERSION = "v201710"


class Client:
    """ AdWords service class that handles interactions with AdWords API and provides a top-level interface for this api.
    Most important functionality:
        - Initiate API connection using credentials
        - Generator for accounts matching the account selector in project _config
        - Download reports
    """
    def __init__(self, credentials_path=DEFAULT_CREDENTIALS_PATH, api_version=DEFAULT_API_VERSION):
        # caution, don't change the order of these attributes
        self._client = self._authenticate(credentials_path)
        self.top_level_account_id = self._client.client_customer_id
        self.api_version = api_version

        self.downloader = self._init_report_downloader()

    def accounts(self):
        """
        :return: generator with Account objects sorted by name
        """
        ad_accounts = self._get_entries(Account.SELECTOR, service="ManagedCustomerService")

        for ad_account in ad_accounts:
            account = Account.from_ad_account(client=self, ad_account=ad_account)
            self.select(account)
            yield account
        self.reset_selection()

    def select(self, obj):
        """ starts a new session with the scope of this account.
        :param obj: str, int or Account
        """
        account_id = to_account_id(obj)
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
    def _authenticate(self, credentials_path):
        return adwords.AdWordsClient.LoadFromStorage(credentials_path)
