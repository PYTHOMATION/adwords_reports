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

    def execute(self, operations):
        """ Uploads a list of operations to adwords api using standard mutate service.
        :return: response from adwords API
        """
        if len(operations) > MAX_OPERATIONS_STANDARD_UPLOAD:
            raise IOError("More than {num} operations. Please use batch upload.")

        operation_type = self.check_operation_type(operations)
        is_label = "Label" in operation_type and operation_type != "LabelOperation"
        if is_label:
            service_name = operation_type.replace("LabelOperation", "Service")
        else:
            service_name = operation_type.replace("Operation", "Service")
        service = self.adwords_service.init_service(service_name)

        self.client.partial_failure = self.partial_failure
        self.client.validate_only = self.is_debug
        print("##### OperationUpload is LIVE: %s. #####" % (not self.client.validate_only))

        result, error_list = self.upload(operations, service, is_label)
        self.print_failures(error_list)
        return result

    @staticmethod
    def check_operation_type(operations):
        operation_types = {operation["xsi_type"] for operation in operations}
        if len(operation_types) != 1:
            raise IOError("Standard upload only supports operations of the same type."
                          "Please use batch upload or multiple standard uploads otherwise.")
        return list(operation_types)[0]  # singular value of set

    @ErrorRetryer()
    def upload(self, operations, service, is_label):
        try:
            if is_label:
                result = service.mutateLabel(operations)
            else:
                result = service.mutate(operations)

            if not self.is_debug and 'partialFailureErrors' in result:
                error_list = result['partialFailureErrors']
            else:
                error_list = list()

        except suds.WebFault as e:
            result = None
            if "detail" not in e.fault:
                error_list = ["is_label error"]  # hack
            else:
                error_list = e.fault.detail.ApiExceptionFault.errors
        finally:
            # reset validate only header so later get calls to API will work
            self.client.validate_only = False
        return result, error_list

    def print_failures(self, error_list):
        """ Printing failed operations + reason using AdWordsError model """
        if not error_list and not self.is_debug:
            print("All operations successfully uploaded.")
        elif error_list == ["is_label error"]:
            print("Please use 'is_label' parameter for uploading label operations with standard upload.")
        else:
            error_texts = list()
            for adwords_error in error_list:
                index = adwords_error["fieldPathElements"][0]["index"]
                error = AdWordsError.from_adwords_error(index=index, adwords_error=adwords_error)
                error_texts.append(error.to_string())
            print("\n".join(error_texts))
