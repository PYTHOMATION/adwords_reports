import suds

from freedan.adwords_services.adwords_error import AdWordsError
from freedan.other_services.error_retryer import ErrorRetryer

MAX_OPERATIONS_STANDARD_UPLOAD = 5000


class StandardUploader:
    """ AdWords service object for standard uploads of mutate operations to AdWords API """
    def __init__(self, adwords_service, is_debug, partial_failure):
        self.adwords_service = adwords_service
        self.client = adwords_service.client
        self.is_debug = is_debug
        self.partial_failure = partial_failure

    def execute(self, operations, service_name, is_label):
        """ Uploads a list of operations to adwords api using standard mutate service.
        :return: response from adwords API
        """
        service = self.adwords_service.init_service(service_name)

        self.client.partial_failure = self.partial_failure
        self.client.validate_only = self.is_debug
        print("##### OperationUpload is LIVE: %s. #####" % (not self.client.validate_only))

        try:
            result = self.upload(operations, service, is_label)
            error_list = list()
            if 'partialFailureErrors' in result:
                error_list = result['partialFailureErrors']
        except suds.WebFault as e:
            result = None
            error_list = e.fault.detail.ApiExceptionFault.errors
        finally:
            # reset validate only header so later API get calls will work
            self.client.validate_only = False

        self.print_failures(error_list)
        return result

    @ErrorRetryer()
    def upload(self, operations, service, is_label):
        if is_label:
            return service.mutateLabel(operations)
        else:
            return service.mutate(operations)

    @staticmethod
    def print_failures(error_list):
        """ Printing failed operations + reason using AdWordsError model """
        error_texts = list()
        for adwords_error in error_list:
            index = adwords_error["fieldPathElements"][0]["index"]
            error = AdWordsError.from_adwords_error(index=index, adwords_error=adwords_error)
            error_texts.append(error.to_string())

        if error_texts:
            print("\n".join(error_texts))
        else:
            print("All operations successfully uploaded.")
