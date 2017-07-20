import os

from freedan import AdWords, TimeInstance
from freedan import base_dir, from_json


class Initiator:
    """ Class taking care of initiation of often used functionality in a project. For instance:
        - Initiate Marketing API
        - Initiating path of output and _config folder
        - Load _config files
        - Initiate TimeInstance object
    """
    def __init__(self, channel, project_name, debug=True, config_name=None):
        """ 
        :param channel: str, needs to match a value used in __init_api_client method
        :param project_name: name of the project, normally matches folder name
        :param debug: bool, normally used as a parameter for upload interactions with Marketing APIs
        :param config_name: needs to be specified if project_name != folder name
        """
        # input properties
        self.channel = channel.lower()
        self.project_name = project_name
        self.config_name = config_name
        self.debug = debug

        # output path and _config
        self.output_path, self.project_config = self.project_info()

        # time
        self.time_instance = TimeInstance()

        # api interaction
        self.api_service = self.__init_api_client()

    def __init_api_client(self):
        """ Initiate Marketing API service object """
        if self.channel == "search":
            return AdWords(report_path=self.output_path)
        else:
            raise IOError("No api service for this channel built yet: %s" % self.channel)

    def project_info(self):
        """ Initiate _config and commonly used paths """
        config_name = self.config_name or "{project_name}.json".format(project_name=self.project_name)

        # paths
        project_path = "{path}/src/projects/{project_name}".format(path=base_dir, project_name=self.project_name)
        output_path = "{project_path}/outputs".format(project_path=project_path)
        config_path = "{project_path}/_config/{config_name}".format(project_path=project_path, config_name=config_name)

        # load _config
        project_config = from_json(config_path)

        # output folder is not pushed to git, so it needs to be created automatically
        self.create_folder_if_not_existing(output_path)

        return output_path, project_config

    @staticmethod
    def create_folder_if_not_existing(path):
        """ Create folder if it's not already existing 
        :param path: str, path of folder
        """
        if not os.path.exists(path):
            os.makedirs(path)

    def construct_path(self, name, with_date=True, with_hour=True, custom_params=list()):
        """ Construct path of output files with certain parameters
        :param name: str, custom name of output file
        :param with_date: bool, if True current date will be added to file name
        :param with_hour: bool, if True current hour will be added to file name (only in combination with date)
        :param custom_params: list, those parameters will also be added to the file name (e.g. acc type, domain, ...)
        :return: str, path of a file
        """
        date = self.time_instance.date_hour_string if with_hour else self.time_instance.date_string
        custom_params = [str(param) for param in custom_params]

        all_parameters = custom_params + [date] + [name] if with_date else custom_params + [name]
        return "{path}/{full_name}.csv".format(path=self.output_path, full_name="_".join(all_parameters))
