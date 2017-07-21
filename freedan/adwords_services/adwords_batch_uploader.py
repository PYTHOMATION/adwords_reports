import collections
import datetime
import time
from urllib.request import urlopen

import pandas as pd

from freedan.adwords_services.adwords_error import AdWordsError
from freedan.other_services.error_retryer import ErrorRetryer


PENDING_STATUSES = ('ACTIVE', 'AWAITING_FILE', 'CANCELING')


class AdWordsBatchUploader:
    """ AdWords service class that handles
        - batch uploads
        - and the related error handling """
    def __init__(self, adwords_service):
        """
        :param adwords_service: AdWords object 
        """
        self.batch_job_helper = adwords_service.batch_job_helper()
        self.batch_job_service = adwords_service.init_service("BatchJobService")
        self.adwords_object = self.__add_batch_job()
        self.upload_url = self.adwords_object["uploadUrl"]["url"]
        self.id = self.adwords_object["id"]
        self.status = None
        self.download_url = None

    @staticmethod
    def fillna_with_temp_id(batchjob_helper, adwords_id):
        """ If id is np.nan, return new temporary id (negative int), else return the id"""
        if pd.isnull(adwords_id):
            return int(batchjob_helper.GetId())
        return adwords_id

    @ErrorRetryer()
    def __add_batch_job(self):
        """ Adding a new BatchJob """
        batch_job_operations = [{
            'operand': {},
            'operator': 'ADD'
        }]
        return self.batch_job_service.mutate(batch_job_operations)['value'][0]

    @ErrorRetryer()
    def upload_operation(self, operations):
        """ Upload operations """
        print(datetime.datetime.now(), "Upload started...")
        self.batch_job_helper.UploadOperations(self.upload_url, *operations)
        print(datetime.datetime.now(), "Upload finished...")

    def report_on_results(self, batch_sleep_interval):
        """ Wait for results of batch upload and download them to report on errors """
        self.__get_batch_job_download_url_when_ready(batch_sleep_interval)

        response_xml = urlopen(self.download_url).read()
        raw_response = self.batch_job_helper.ParseResponse(response_xml)
        errors = self.__report_on_partial_errors(raw_response)
        return raw_response, errors

    @ErrorRetryer()
    def __get_batch_job_download_url_when_ready(self, batch_sleep_interval):
        """ Attempts to fetch BatchJob download url multiple times. Sleeps for x seconds in between attempts """
        self.__update_attributes()
        poll_attempt = 0  # needed for sleep duration calculation
        while self.status in PENDING_STATUSES:
            self.sleep_if_not_ready(poll_attempt, batch_sleep_interval)
            self.__update_attributes()
            poll_attempt += 1

            if self.download_url is not None:
                return self.download_url

    @ErrorRetryer()
    def __update_attributes(self):
        """ Get existing BatchJob by id. Including download url """
        selector = {
            'fields': ['Id', 'Status', 'DownloadUrl'],
            'predicates': [{
                'field': 'Id',
                'operator': 'EQUALS',
                'values': [self.id]
            }]
        }
        batch_job = self.batch_job_service.get(selector)['entries'][0]
        self.adwords_object = batch_job
        self.id = batch_job["id"]
        self.status = batch_job["status"] if "status" in batch_job else None
        self.download_url = batch_job["downloadUrl"]["url"] if "downloadUrl" in batch_job else None

    @staticmethod
    def sleep_if_not_ready(poll_attempt, batch_sleep_interval):
        """ Determine sleep interval for batch job """
        exponential = min(300, 30 * 2**poll_attempt)
        seconds = exponential if batch_sleep_interval == -1 else batch_sleep_interval

        minutes = int(round(float(seconds) / 60.0))
        print("Operations are being processed by AdWords."
              "Sleeping for {s} seconds (~{m} minutes).".format(s=seconds, m=minutes))
        time.sleep(seconds)

    @staticmethod
    def __report_on_partial_errors(response):
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

        error_message = "\n".join(all_error_texts) or "All operations successfully uploaded."
        print(error_message)

        if error_summary:
            summary_message = "\n".join(["{type}: {count}".format(type=sub_type, count=len(indexes))
                                         for sub_type, indexes in error_summary.items()])
            print("\nSummary:")
            print(summary_message)
        return all_errors
