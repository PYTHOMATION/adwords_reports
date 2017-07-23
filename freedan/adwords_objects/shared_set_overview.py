DEFAULT_TYPES = ["NEGATIVE_KEYWORDS"]


class SharedSetOverview:
    """ Shared sets contain negative keywords/placements that can be shared across campaigns or accounts.
    They can only be applied on Campaign level though.
    
    This class provides an overview of all shared sets (+id) for specific types (e.g. negative keywords).
    Those ids are normally used in other campaign operations later on. 
    """
    def __init__(self, adwords_service, set_types=DEFAULT_TYPES):
        self.overview = self._download_overview(adwords_service, set_types)

    @staticmethod
    def _download_overview(adwords_service, set_types):
        """ Query an overview of shared sets from AdWords API.
        :param adwords_service: AdWords object
        :param set_types: list of str, e.g. negative keywords, negative placements, ...
        :return: dataframe
        """
        report_definition = {
            "reportName": "name",
            "dateRangeType": "LAST_7_DAYS",
            "reportType": "SHARED_SET_REPORT",
            "downloadFormat": "CSV",
            "selector": {
                "fields": ["Name", "SharedSetId"],
                "predicates": [{
                    "field": "Status",
                    "operator": "NOT_EQUALS",
                    "values": "REMOVED"
                }, {
                    "field": "Type",
                    "operator": "IN",
                    "values": set_types
                }]
            }
        }
        shared_sets = adwords_service.download_report(report_definition, include_0_imp=True)\
            .rename(columns={"Name": "SharedSetName"})
        return shared_sets
