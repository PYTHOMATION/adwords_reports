from py_adwords_reports import AdWordsClient


def account_hierarchy(credentials):
    """
    This script will loop over your accounts and print out their names.
    :param credentials: str, path to your adwords credentials file
    """
    # init connection to adwords API
    client = AdWordsClient(credentials)

    # before the method is returning an account it 'selects' it,
    # i.e. it creates a new session with the scope of this account.
    for account in client.accounts():
        print(account)


if __name__ == "__main__":
    credentials_path = "googleads.yaml"
    account_hierarchy(credentials_path)
