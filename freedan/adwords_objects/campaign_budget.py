import uuid

from freedan.adwords_services.adwords_service import AdWordsService


class CampaignBudget:
    """ CampaignBudget. A budget is mandatory when creating a new campaign """
    def __init__(self, amount, is_shared=False, name=None):
        self.amount, self.micro_amount = AdWordsService.reg_and_micro(amount)
        self.name = name or 'API Budget #{uuid}'.format(uuid=uuid.uuid4().int)
        self.is_shared = is_shared

    def add_operation(self, temp_id=None, delivery="ACCELERATED"):
        """ Add operation for AdWords API"""
        operation = {
            "xsi_type": "BudgetOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "Budget",
                "amount": {
                    "microAmount": self.micro_amount
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
