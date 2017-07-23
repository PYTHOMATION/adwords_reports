from tests import service_suds_client


def account():
    suds_client = service_suds_client("ManagedCustomerService")

    # create labels
    labels = list()
    for i, name in enumerate(["test1", "this_is_a_label"]):
        label = suds_client.factory.create("AccountLabel")
        label.id = i
        label.name = name
        labels.append(label)

    # create ad_account
    ad_account = suds_client.factory.create("ManagedCustomer")
    ad_account.name = "Test1"
    ad_account.customerId = "302-203-1203"
    ad_account.canManageClients = False
    ad_account.currencyCode = "CAD"
    ad_account.dateTimeZone = "America/Vancouver"
    ad_account.testAccount = False
    ad_account.accountLabels = labels
    return ad_account

