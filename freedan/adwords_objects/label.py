DEFAULT_TEMP_LABEL_ID = -999999


class Label:
    """ AdWords service class for handling of labels (inside accounts). Those can be applied to
        - Campaigns
        - AdGroups
        - Keywords
    """
    def __init__(self, text):
        self.text = text
        self.id = None

    def update_id(self, adwords_service, is_debug):
        """ Get id of this label text inside the current account.
            If the label isn't existing yet:
                if debug=False: it will be created 
                else:           a default value is returned
        """
        label_page = self.fetch_id_from_adwords(adwords_service)

        if "entries" in label_page:
            label_id = label_page["entries"][0].id
        elif not is_debug:
            result = self.create_label(adwords_service)
            label_id = result["value"][0]["id"]
        else:
            label_id = DEFAULT_TEMP_LABEL_ID
        
        self.id = label_id
        return self.id
    
    def fetch_id_from_adwords(self, adwords_service):
        label_selector = {
            "fields": ["LabelId"],
            "predicates": [{
                "field": "LabelName",
                "operator": "EQUALS",
                "values": self.text
            }]
        }
        return adwords_service._get_page(label_selector, "LabelService")

    def create_label(self, adwords_service):
        """ Creates the label via standard upload to AdWords API """
        operation = [self.add_operation()]
        print("Creating label %s" % self.text)
        return adwords_service.execute(operation, debug=False, service="LabelService")

    def add_operation(self):
        """ Operation to add a label object in AdWords """
        operation = {
            "xsi_type": "LabelOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "TextLabel",
                "name": self.text
            }
        }
        return operation

    def apply_on_adgroup_operation(self, adgroup_id):
        """ Apply label to AdGroup operation """
        operation = {
            "xsi_type": "AdGroupLabelOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "AdGroupLabel",
                "adGroupId": adgroup_id,
                "labelId": self.id,
            }
        }
        return operation

    def apply_on_keyword_operation(self, adgroup_id, criterion_id):
        """ Apply label to Keyword operation """
        operation = {
            "xsi_type": "AdGroupCriterionLabelOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "AdGroupCriterionLabel",
                "adGroupId": adgroup_id,
                "criterionId": criterion_id,
                "labelId": self.id,
            }
        }
        return operation
