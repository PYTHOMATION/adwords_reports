class Account:
    """ Adding some business specific information to AdWords internal account object """
    def __init__(self, ad_account, account_id, name):
        self.ad_account = ad_account
        self.name = name
        self.id = account_id

    @classmethod
    def from_ad_account(cls, ad_account):
        """ Construct object only from adwords account object
        :param ad_account: internal AdWords account object
        :return: SearchAccount object
        """
        name = ad_account.name
        account_id = ad_account.customerId
        return cls(ad_account=ad_account, account_id=account_id, name=name)

    @classmethod
    def from_name(cls, name):
        """ Construct object only from name """
        return cls(ad_account=None, account_id=None, name=name)

    def __repr__(self):
        """ user friendly readable string representation """
        representation = "\nAccountName: {name} (ID: {id})\n".format(name=self.name, id=self.id)
        return representation
