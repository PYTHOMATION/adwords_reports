import freedan


credentials_path = "adwords_credentials.yaml"
adwords_service = freedan.AdWordsService(credentials_path)

for account in adwords_service.accounts():
    print(account)
