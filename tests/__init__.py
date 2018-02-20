import os
import pytest

from adwords_reports.client import Client

test_dir = os.path.dirname(__file__)


adgroup1_name = "Ad Group #1"
adgroup1_id = 47391167467


@pytest.fixture()
def fix_client():
    test_credentials = os.path.join(test_dir, "test_googleads.yaml")
    return Client(test_credentials)


@pytest.fixture()
def fix_account_service(fix_client):
    service = fix_client._init_service("ManagedCustomerService")
    return service.suds_client


@pytest.fixture()
def fix_adwords_account_label(fix_account_service, name, label_id):
    label = fix_account_service.factory.create("AccountLabel")
    label.name = name
    label.id = label_id
    return label


@pytest.fixture()
def fix_native_adwords_account(fix_account_service):
    ad_account = fix_account_service.factory.create("ManagedCustomer")
    ad_account.name = "Test1"
    ad_account.customerId = "302-203-1203"
    ad_account.currencyCode = "CAD"
    ad_account.dateTimeZone = "America/Vancouver"
    ad_account.canManageClients = False
    ad_account.testAccount = False
    ad_account.accountLabels = [
        fix_adwords_account_label("test1", 0),
        fix_adwords_account_label("this_is_a_label", 1)
    ]
    return ad_account
