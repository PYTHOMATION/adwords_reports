import os
import pytest

from adwords_reports.client import Client
from adwords_reports.account_label import AccountLabel

test_dir = os.path.dirname(__file__)


@pytest.fixture()
def fix_client():
    test_credentials = os.path.join(test_dir, "test_googleads.yaml")
    return Client(test_credentials)


@pytest.fixture()
def fix_account(fix_client):
    return list(fix_client.accounts())[0]


@pytest.fixture()
def fix_adwords_account_service(fix_client):
    service = fix_client._init_service("ManagedCustomerService")
    return service.suds_client


@pytest.fixture()
def fix_adwords_account_label(fix_adwords_account_service):
    label = fix_adwords_account_service.factory.create("AccountLabel")
    label.name = "unused"
    label.id = 123
    return label


@pytest.fixture()
def fix_adwords_account(fix_adwords_account_service, fix_adwords_account_label):
    ad_account = fix_adwords_account_service.factory.create("ManagedCustomer")
    ad_account.name = "Test1"
    ad_account.customerId = "519-085-5164"
    ad_account.currencyCode = "CAD"
    ad_account.dateTimeZone = "America/Vancouver"
    ad_account.canManageClients = False
    ad_account.testAccount = False
    ad_account.accountLabels = [
        fix_adwords_account_label
    ]
    return ad_account


@pytest.fixture()
def fix_account_label(fix_adwords_account_label):
    return AccountLabel.from_ad_account_label(fix_adwords_account_label)


@pytest.fixture()
def fix_report_definition():
    from adwords_reports.report_definition import ReportDefinition
    return ReportDefinition(report_type="KEYWORDS_PERFORMANCE_REPORT", fields=["Criteria"], last_days=7)
