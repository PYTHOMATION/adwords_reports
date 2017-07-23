from tests import service_suds_client


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


def test_account_label():
    from freedan import AccountLabel

    adwords_label = init_native_adwords_account_label("test_acc_label", 90)
    acc_label = AccountLabel.from_adwords_account_label(adwords_label)
    assert acc_label.name == "test_acc_label"
    assert acc_label.id == 90


def test_account():
    from freedan import Account, AccountLabel

    # test initiation from native adwords account
    adwords_account = init_native_adwords_account()
    account = Account.from_ad_account(ad_account=adwords_account)
    assert account.name == "Test1"
    assert account.id == "302-203-1203"
    assert account.currency == "CAD"
    assert account.time_zone == "America/Vancouver"
    assert not account.is_mcc
    assert not account.is_test

    # check labels
    assert all(isinstance(e, AccountLabel) for e in account.labels)
    label1, label2 = account.labels
    assert (label1.name, label1.id) == ("test1", 0)
    assert (label2.name, label2.id) == ("this_is_a_label", 1)

    # test initiation from name
    account = Account.from_name("Test2")
    assert account.name == "Test2"
    assert account.id is None
    assert account.currency is None
    assert account.time_zone is None
    assert account.is_mcc is None
    assert account.is_test is None
    assert account.labels is None
