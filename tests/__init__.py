import os
from freedan.adwords_services.adwords_service import AdWordsService

test_dir = os.path.dirname(__file__)
adwords_test_credentials = os.path.join(test_dir, "adwords_test_credentials.yaml")

adwords_service = AdWordsService(adwords_test_credentials)


def service_suds_client(service_name):
    service = adwords_service.init_service(service_name)
    return service.suds_client
