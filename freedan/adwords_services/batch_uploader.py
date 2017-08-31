import datetime
import time
import collections
from urllib.request import urlopen
import pandas as pd

from freedan.adwords_services.adwords_error import AdWordsError
from freedan.other_services.error_retryer import ErrorRetryer


PENDING_STATUSES = ('ACTIVE', 'AWAITING_FILE', 'CANCELING')


class BatchUploader:
    """ AdWords service class that handles
        - batch uploads
        - and the related error handling
    """
    def __init__(self, adwords_service, is_debug, report_on_results=True, batch_sleep_interval=-1):
        self.adwords_service = adwords_service
        self.batch_job_service = adwords_service.init_service("BatchJobService")
        self.batch_job_helper = self.batch_job_helper()

        self.is_debug = is_debug
        self.report_on_results = report_on_results
        self.batch_sleep_interval = batch_sleep_interval

        self.batch_job = self._add_batch_job()
        # # memo for important attributes of batch job
        # batch_job.uploadUrl.url
        # batch_job.id
        # batch_job.status
        # batch_job.downloadUrl.url

    @ErrorRetryer()
    def batch_job_helper(self):
        """ Get an AdWords BatchJobHelper object
        E.g. for temporary ids """
        client = self.adwords_service.client
        api_version = self.adwords_service.api_version
        return client.GetBatchJobHelper(version=api_version)

    @ErrorRetryer()
    def _add_batch_job(self):
        """ Adding a new BatchJob """
        batch_job_operations = [{
            'operand': {},
            'operator': 'ADD'
        }]
        return self.batch_job_service.mutate(batch_job_operations)['value'][0]

    def execute(self, operations):
        """ Uploads a batch of operations to adwords api using batch job service.
        :param operations: tuple of lists of operations
        :return: return value of adwords
        """
        print("Uploading operations using BatchJob")
        print("##### OperationUpload is LIVE: {is_live}. #####".format(is_live=(not self.is_debug)))

        if not self.is_debug:
            self._upload(operations)

            if self.report_on_results:
                self._get_batch_job_download_url_when_ready(self.batch_sleep_interval)
                raw_response = self._read_response()
                errors = self._parse_partial_failures(raw_response)
                return raw_response, errors
        else:
            print("Operations couldn't be validated since AdWords' BatchUpload doesn't support validate only header")
        return None

    @ErrorRetryer()
    def _upload(self, operations):
        """ Upload operations """
        print(datetime.datetime.now(), "Upload started...")
        self.batch_job_helper.UploadOperations(self.batch_job.uploadUrl.url, *operations)
        print(datetime.datetime.now(), "Upload finished...")

    @ErrorRetryer()
    def _get_batch_job_download_url_when_ready(self, batch_sleep_interval):
        """ Attempts to fetch BatchJob download url multiple times. Sleeps for x seconds in between attempts """
        self._update_attributes()
        poll_attempt = 0  # needed for sleep duration calculation
        while self.batch_job.status in PENDING_STATUSES:
            self._sleep_if_not_ready(poll_attempt, batch_sleep_interval)
            self._update_attributes()
            poll_attempt += 1

            if "downloadUrl" in self.batch_job:
                return self.batch_job.downloadUrl.url

    @staticmethod
    def _sleep_if_not_ready(poll_attempt, batch_sleep_interval):
        """ Determine sleep interval for batch job """
        exponential = min(300, 30 * 2**poll_attempt)
        seconds = exponential if batch_sleep_interval == -1 else batch_sleep_interval

        minutes = int(round(float(seconds) / 60.0))
        print("Operations are being processed by AdWords."
              "Sleeping for {s} seconds (~{m} minutes).".format(s=seconds, m=minutes))
        time.sleep(seconds)

    @ErrorRetryer()
    def _update_attributes(self):
        """ Get existing BatchJob by id. Including download url """
        selector = {
            'fields': ['Id', 'Status', 'DownloadUrl'],
            'predicates': [{
                'field': 'Id',
                'operator': 'EQUALS',
                'values': [self.batch_job.id]
            }]
        }
        self.batch_job = self.batch_job_service.get(selector)['entries'][0]

    def _read_response(self):
        """ Wait for results of batch upload and download them to report on errors """
        response_xml = urlopen(self.batch_job.downloadUrl.url).read()
        return self.batch_job_helper.ParseResponse(response_xml)

    @staticmethod
    def _parse_partial_failures(response):
        """ Parses the XML response of the BatchJob and reports on errors. """
        error_summary = collections.defaultdict(set)
        all_errors = list()
        all_error_texts = list()
        if "rval" in response["mutateResponse"]:
            return_values = response["mutateResponse"]["rval"]
            if not isinstance(return_values, list):
                return_values = [return_values]
            for data in return_values:
                if "index" in data and "errorList" in data and "errors" in data["errorList"]:
                    index = data["index"]
                    adwords_errors = data["errorList"]["errors"]
                    if not isinstance(adwords_errors, list):
                        adwords_errors = [adwords_errors]

                    for adwords_error in adwords_errors:
                        error = AdWordsError.from_adwords_error(index=index, adwords_error=adwords_error)

                        all_errors.append(error)
                        all_error_texts.append(error.to_string())

                        error_summary[error.sub_type].add(index)  # count on how many operations an error type occurred

        if all_error_texts:
            print("\n".join(all_error_texts))
        else:
            print("All operations successfully uploaded.")

        if error_summary:
            summary_message = "\n".join(["{type}: {count}".format(type=sub_type, count=len(indexes))
                                         for sub_type, indexes in error_summary.items()])
            print("\nSummary:")
            print(summary_message)
        return all_errors
