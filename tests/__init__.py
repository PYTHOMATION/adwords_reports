from freedan.adwords_services.adwords import AdWords

adwords_test_credentials = "adwords_test_credentials.yaml"

adwords_service = AdWords(adwords_test_credentials)


def service_suds_client(service_name):
    service = adwords_service.init_service(service_name)
    return service.suds_client
