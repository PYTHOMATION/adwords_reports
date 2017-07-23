from freedan.adwords_objects.account_label import AccountLabel


class Account:
    """ Adding some business specific information to AdWords internal account object """
    def __init__(self, ad_account, account_id, name, is_mcc, currency, time_zone, is_test, labels):
        self.ad_account = ad_account
        self.name = name
        self.id = account_id
        self.time_zone = time_zone
        self.currency = currency
        self.is_mcc = is_mcc
        self.is_test = is_test
        self.labels = labels

    @classmethod
    def from_ad_account(cls, ad_account):
        """ Construct object only from adwords account object
        :param ad_account: internal AdWords account object
        :return: SearchAccount object
        """
        labels = list()
        if "accountLabels" in ad_account:
            for adwords_label in ad_account.accountLabels:
                label = AccountLabel.from_adwords_account_label(adwords_label)
                labels.append(label)

        return cls(ad_account=ad_account, account_id=ad_account.customerId, name=ad_account.name,
                   is_mcc=ad_account.canManageClients, currency=ad_account.currencyCode,
                   time_zone=ad_account.dateTimeZone, is_test=ad_account.testAccount, labels=labels)

    @classmethod
    def from_name(cls, name):
        """ Construct object only from name """
        return cls(ad_account=None, account_id=None, name=name, is_mcc=None,
                   currency=None, time_zone=None, is_test=None, labels=None)

    def __repr__(self):
        """ user friendly readable string representation """
        representation = "\nAccountName: {name} (ID: {id})".format(name=self.name, id=self.id)
        return representation
