DEFAULT_TEMP_LABEL_ID = -999999


class Label:
    """ AdWords service class for handling of labels (inside accounts). Those can be applied to
        - Campaigns
        - AdGroups
        - Keywords
    """
    def __init__(self, text, adwords_service, debug=True):
        """
        :param text: str, text of the label (there's a maximum size, but I don't know it)
        :param adwords_service: AdWords object
        :param debug: bool
        """
        self.text = text
        self.adwords_service = adwords_service
        self.id = self.get_id(debug)

    def get_id(self, debug):
        """ Get id of this label text inside the current account.
            If the label isn't existing yet:
                if debug=False: it will be created 
                else:           a default value is returned
        """
        label_selector = {
            'fields': ['LabelId'],
            'predicates': [{
                'field': 'LabelName',
                'operator': 'EQUALS',
                'values': self.text
            }]
        }
        label_page = self.adwords_service._get_page(label_selector, "LabelService")

        if 'entries' in label_page:
            return label_page['entries'][0].id
        elif not debug:
            result = self.create_label()
            return result['value'][0]['id']
        else:
            return DEFAULT_TEMP_LABEL_ID

    def create_label(self):
        """ Creates the label via standard upload to AdWords API """
        operation = [self.add_operation()]
        print("Creating label %s" % self.text)
        return self.adwords_service.execute(operation, debug=False, service="LabelService")

    def add_operation(self):
        """ Operation to add a label object in AdWords """
        operation = {
            'xsi_type': 'LabelOperation',
            'operator': 'ADD',
            'operand': {
                'xsi_type': "TextLabel",
                'name': self.text
            }
        }
        return operation

    def apply_on_adgroup_operation(self, adgroup_id):
        """ Apply label to AdGroup operation """
        operation = {
            'xsi_type': 'AdGroupLabelOperation',
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'AdGroupLabel',
                'adGroupId': adgroup_id,
                'labelId': self.id,
            }
        }
        return operation

    def apply_on_keyword_operation(self, adgroup_id, criterion_id):
        """ Apply label to Keyword operation """
        operation = {
            'xsi_type': 'AdGroupCriterionLabelOperation',
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'AdGroupCriterionLabel',
                'adGroupId': adgroup_id,
                'criterionId': criterion_id,
                'labelId': self.id,
            }
        }
        return operation
