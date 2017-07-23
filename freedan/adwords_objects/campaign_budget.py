import uuid

from freedan.adwords_services.adwords_service import AdWordsService


class CampaignBudget:
    """ CampaignBudget. A budget is mandatory when creating a new campaign """
    def __init__(self, amount, convert_to_micro=True, is_shared=False, name=None):
        self.amount = AdWordsService.euro_to_micro(amount) if convert_to_micro else amount
        self.name = name or 'API Budget #{uuid}'.format(uuid=uuid.uuid4().int)
        self.is_shared = is_shared

    def add_operation(self, temp_id=None, delivery="ACCELERATED"):
        """ Add operation for AdWords API"""
        assert self.amount >= 10000  # i.e. >= 1 cent

        operation = {
            "xsi_type": "BudgetOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "Budget",
                "amount": {
                    "microAmount": self.amount
                },
                "deliveryMethod": delivery,
                "isExplicitlyShared": self.is_shared
            }
        }
        if self.name is not None:
            operation["operand"]["name"] = self.name,
        if temp_id is not None:
            operation["operand"]["budgetId"] = temp_id
        return operation
