class Account:
    """ Adding some business specific information to AdWords internal account object """
    def __init__(self, ad_account, account_id, name, can_manage_clients, currency, time_zone, is_test_account):
        self.ad_account = ad_account
        self.name = name
        self.id = account_id
        self.time_zone = time_zone
        self.currency = currency
        self.can_manage_clients = can_manage_clients
        self.is_test_account = is_test_account

    @classmethod
    def from_ad_account(cls, ad_account):
        """ Construct object only from adwords account object
        :param ad_account: internal AdWords account object
        :return: SearchAccount object
        """
        return cls(ad_account=ad_account, account_id=ad_account.customerId, name=ad_account.name,
                   can_manage_clients=ad_account.canManageClients, currency=ad_account.currencyCode,
                   time_zone=ad_account.dateTimeZone, is_test_account=ad_account.testAccount)

    @classmethod
    def from_name(cls, name):
        """ Construct object only from name """
        return cls(ad_account=None, account_id=None, name=name)

    def __repr__(self):
        """ user friendly readable string representation """
        representation = "\nAccountName: {name} (ID: {id})".format(name=self.name, id=self.id)
        return representation
