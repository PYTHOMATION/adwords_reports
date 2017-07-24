import freedan


def account_hierarchy(credentials_path):
    """
    This script will loop over your accounts and print out the names of all accounts.
    By default MCC accounts will be skipped. You can change this by changing the 'skip_mcc' parameter
    :param credentials_path: str, path to your adwords credentials file
    """

    # init connection to adwords API
    adwords_service = freedan.AdWordsService(credentials_path)

    # access your accounts
    for account in adwords_service.accounts():
        print(account)


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    account_hierarchy(adwords_credentials_path)
