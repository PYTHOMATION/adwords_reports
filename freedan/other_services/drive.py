import io
import os
import apiclient
import httplib2
import oauth2client.file
import pandas as pd
import pygsheets
from googleapiclient.http import MediaIoBaseDownload
from xlsxwriter.utility import xl_col_to_name

from freedan import ErrorRetryer
from freedan import config

MAX_ATTEMPTS = config["max_attempts"]
SLEEP_INTERVAL = config["sleep_interval"]


class Drive:
    """ Google Drive service object. Can interact with Google Drive and Google Sheets
    (natively they use different Google APIs)
    """
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        self.drive_service = self.initiate_api_connection("drive")
        self.sheet_service = self.initiate_api_connection("sheets")

    @ErrorRetryer(MAX_ATTEMPTS, SLEEP_INTERVAL)
    def initiate_api_connection(self, product):
        """
        Provides the according service to work with Google Sheets
        :return: service object
        """
        credentials = oauth2client.file.Storage(self.credentials_path).get()
        http = credentials.authorize(httplib2.Http())

        if product == "sheets":
            discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
            return apiclient.discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

        elif product == "drive":
            return apiclient.discovery.build('drive', 'v3', http=http)

        else:
            raise IOError("Unexpected product.")

    @ErrorRetryer(MAX_ATTEMPTS, SLEEP_INTERVAL)
    def worksheet_values(self, spreadsheet_id, data_range):
        """ Downloads data from a google work sheet and returns it as pandas dataframe
        :param spreadsheet_id: str
        :param data_range: str
        :return: dataframe
        """
        # Fetch data from Drive
        result = self.sheet_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=data_range).execute()

        # Load into DataFrame
        header = result["values"][0]
        data = result["values"][1:]

        # exception handling if last column is empty (since data and header have different format then...)
        for line in data:
            for missing_item in range(len(header) - len(line)):
                line.append(pd.np.nan)

        df = pd.DataFrame(data, columns=header)
        return df

    @ErrorRetryer(MAX_ATTEMPTS, SLEEP_INTERVAL)
    def sheet_names(self, spreadsheet_id):
        """
        :param: spreadsheet_id: id of the spreadsheet
        :return: list of str, containing all work sheet names in the drive 
        """
        gc = pygsheets.authorize(outh_file=self.credentials_path)
        worksheets = gc.open_by_key(spreadsheet_id).worksheets()
        return [worksheet.title for worksheet in worksheets]

    @ErrorRetryer(MAX_ATTEMPTS, SLEEP_INTERVAL)
    def download_csv(self, folder_id, file_name, destination_path, return_data_frame=True):
        """ Downloads a csv file from google drive.
        CAUTION: If return_data_frame=true local csv will be deleted
        :param folder_id: str, folder id of google drive
        :param file_name: str, name of the file in google drive
        :param destination_path: str, credentials path where csv should be saved
        :param return_data_frame: bool
        :return: dataframe
        """
        # get file Id
        query = "'%s' in parents and name = '%s'" % (folder_id, file_name)
        response = self.drive_service.files().list(q=query).execute()
        try:
            file_id = response.get('files', [])[0].get('id')
        except IndexError:
            raise IOError("Couldn't find input file in the Drive Folder: %s" % file_name)

        request = self.drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        while True:
            status, done = downloader.next_chunk()
            print("\tDownloaded %d%%." % int(status.progress() * 100))
            if done:
                break
        data = fh.getvalue()

        if data:
            with open(destination_path, mode="wb") as f:
                f.write(data)

        if return_data_frame:
            values = pd.read_csv(destination_path, encoding="utf8")
            os.remove(destination_path)
            return values

    def dataframe_to_sheets(self, df, spreadsheet_id, sheet_name):
        """ Upload DataFrame to specified Google Sheet
        CAUTION: Won't clean the sheet beforehand
        """
        nested_list = self.dataframe_to_nested_list(df)
        value_range = self.a1_notation(nested_list, sheet_name)
        body = {'values': nested_list}

        self.sheet_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=value_range,
            valueInputOption="USER_ENTERED", body=body).execute()

    @staticmethod
    def dataframe_to_nested_list(df):
        """ Converts dataframe to nested list (2dimensional). Needed for uploads to Google Drive """
        header = list(df.columns)
        nested_list = [list(row) for row in df.itertuples(index=False)]
        return [header] + nested_list

    @staticmethod
    def a1_notation(values, sheet_name):
        """ Get A1 notation associated with the size of values
        :param values: list of lists representing 2d array
        :param sheet_name: Google Drive sheet name
        :return: str, representing the range of AdWords
        """
        assert isinstance(values, list)
        assert isinstance(values[0], list)
        num_cols = len(values[0])
        col_name = xl_col_to_name(num_cols-1)
        return "{sheet_name}!A1:{col}".format(sheet_name=sheet_name, col=col_name)
