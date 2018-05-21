from retrying import retry
from googleads import adwords

from adwords_reports import logger
from adwords_reports.account import Account


DEFAULT_API_VERSION = "v201802"


class Client:
    """ AdWords service class that handles interactions with AdWords API and provides a top-level interface for this api.
    Most important functionality:
        - Initiate API connection using credentials
        - Generator for accounts matching the account selector in project _config
        - Download reports
    """
    def __init__(self, credentials_path, api_version=DEFAULT_API_VERSION):
        # caution, don't change the order of these attributes
        self._client = self._authenticate(credentials_path)
        self.top_level_account_id = self._client.client_customer_id
        self.api_version = api_version

        self.downloader = self._init_report_downloader()

    def accounts(self):
        """
        :return: generator with Account objects sorted by name
        """
        logger.info("Getting accounts.")
        ad_accounts = self._get_entries(Account.SELECTOR, service="ManagedCustomerService")

        for ad_account in ad_accounts:
            account = Account.from_ad_account(client=self, ad_account=ad_account)
            self.select(account_id=account.id)
            yield account
        self.reset_selection()

    def select(self, account_id):
        """ starts a new session with the scope of this account.
        :param account_id: str or int
        """
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

    @retry(stop_max_attempt_number=3, wait_random_min=5000, wait_random_max=10000)
    def _get_page(self, selector, service):
        """
        :param selector: nested dict that describes what is requested
        :param service: str, identifying adwords service that is responsible
        :return: adwords page object
        """
        service_object = self._init_service(service)
        return service_object.get(selector)

    @retry(stop_max_attempt_number=3, wait_random_min=5000, wait_random_max=10000)
    def _init_service(self, service_name):
        logger.info("Initiating {}".format(service_name))
        return self._client.GetService(service_name, version=self.api_version)

    @retry(stop_max_attempt_number=3, wait_random_min=5000, wait_random_max=10000)
    def _init_report_downloader(self):
        logger.info("Initiating ReportDownloader.")
        return self._client.GetReportDownloader(version=self.api_version)

    @retry(stop_max_attempt_number=3, wait_random_min=5000, wait_random_max=10000)
    def _authenticate(self, credentials_path):
        logger.info("Initiating Client.")
        return adwords.AdWordsClient.LoadFromStorage(credentials_path)
