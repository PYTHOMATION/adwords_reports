import os
from adwords_reports.client import Client

test_dir = os.path.dirname(__file__)
adwords_test_credentials = os.path.join(test_dir, "test_googleads.yaml")
test_client = Client(adwords_test_credentials)

adgroup1_name = "Ad Group #1"
adgroup1_id = 47391167467


def service_suds_client(service_name):
    service = test_client._init_service(service_name)
    return service.suds_client


def init_native_adwords_account_label(name, label_id):
    suds_client = service_suds_client("ManagedCustomerService")
    label = suds_client.factory.create("AccountLabel")
    label.name = name
    label.id = label_id
    return label


def init_native_adwords_account():
    suds_client = service_suds_client("ManagedCustomerService")

    # create ad_account
    ad_account = suds_client.factory.create("ManagedCustomer")
    ad_account.name = "Test1"
    ad_account.customerId = "302-203-1203"
    ad_account.currencyCode = "CAD"
    ad_account.dateTimeZone = "America/Vancouver"
    ad_account.canManageClients = False
    ad_account.testAccount = False
    ad_account.accountLabels = [
        init_native_adwords_account_label("test1", 0),
        init_native_adwords_account_label("this_is_a_label", 1)
    ]
    return ad_account
