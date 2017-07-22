import suds

from freedan.adwords_services.adwords_error import AdWordsError
from freedan.other_services.error_retryer import ErrorRetryer

MAX_OPERATIONS_STANDARD_UPLOAD = 5000


class AdWordsStandardUploader:
    """ AdWords service object for standard uploads of operations to AdWords API """
    def __init__(self, adwords_service, service_text, operations, is_debug, is_partial_failure, is_label):
        """
        :param adwords_service: AdWords object
        :param service_text: adwords service object associated with the operations
        :param operations: list of operations
        :param is_debug: bool
        :param is_partial_failure: bool
        :param is_label: bool 
        """
        assert isinstance(operations, list)

        self.client = adwords_service.client
        self.service = adwords_service.init_service(service_text)
        self.operations = operations
        self.is_debug = is_debug
        self.is_partial_failure = is_partial_failure
        self.is_label = is_label

    def execute(self):
        """ Uploads a list of operations to adwords api using standard mutate service.
        :return: response from adwords API
        """
        self.client.partial_failure = self.is_partial_failure
        self.client.validate_only = self.is_debug
        print("##### OperationUpload is LIVE: %s. #####" % (not self.client.validate_only))

        result = None
        try:
            result = self.upload()
        except suds.WebFault as e:
            error_list = e.fault.detail.ApiExceptionFault.errors
            self.print_failures(error_list)
        finally:
            # reset validate only header so further API (read) calls will work
            self.client.validate_only = False

        if result is None and (not self.is_debug):
            print("All operations successfully uploaded.")
        elif result is not None and self.is_partial_failure and 'partialFailureErrors' in result:
            error_list = result['partialFailureErrors']
            self.print_failures(error_list)
        return result

    @ErrorRetryer()
    def upload(self):
        if self.is_label:
            return self.service.mutateLabel(self.operations)
        else:
            return self.service.mutate(self.operations)

    @staticmethod
    def print_failures(error_list):
        """ Printing failed operations + reason using AdWordsError model """
        error_texts = list()
        for adwords_error in error_list:
            index = adwords_error["fieldPathElements"][0]["index"]
            error = AdWordsError.from_adwords_error(index=index, adwords_error=adwords_error)
            error_texts.append(error.to_string())

        error_message = "\n".join(error_texts) or "All operations successfully uploaded."
        print(error_message)
