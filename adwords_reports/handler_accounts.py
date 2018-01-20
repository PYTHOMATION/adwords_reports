ACCOUNT_SELECTOR = {
    "fields": ["Name", "CustomerId", "CurrencyCode", "DateTimeZone"],
    "predicates": [{
        "field": "CanManageClients",
        "operator": "EQUALS",
        "values": "FALSE"
    }],
    "ordering": [{
        "field": "Name",
        "sortOrder": "ASCENDING"
    }]
}


def to_account_id(account_or_id):
    if isinstance(account_or_id, Account):
        return account_or_id.id
    return account_or_id


class Account:
    def __init__(self, account_id, name, currency, time_zone, labels):
        self.name = name
        self.id = account_id
        self.time_zone = time_zone
        self.currency = currency
        self.labels = labels

    @classmethod
    def from_ad_account(cls, ad_account):
        labels = cls.parse_labels(ad_account)
        return cls(account_id=ad_account.customerId, name=ad_account.name,
                   currency=ad_account.currencyCode, time_zone=ad_account.dateTimeZone,
                   labels=labels)

    @staticmethod
    def parse_labels(ad_account):
        if "accountLabels" in ad_account:
            return [AccountLabel.from_ad_account_label(ad_label)
                    for ad_label in ad_account["accountLabels"]]
        return list()

    def __repr__(self):
        return "\nAccountName: {name} (ID: {id})".format(name=self.name, id=self.id)


class AccountLabel:
    def __init__(self, name, label_id):
        self.id = label_id
        self.name = name

    @classmethod
    def from_ad_account_label(cls, adwords_acc_label):
        return cls(name=adwords_acc_label.name, label_id=adwords_acc_label.id)

    def __repr__(self):
        return "{name} ({id})".format(name=self.name, id=self.id)
