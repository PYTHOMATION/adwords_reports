import uuid

from freedan.adwords_services.adwords_service import AdWordsService


class CampaignBudget:
    """ CampaignBudget. A budget is mandatory when creating a new campaign """
    def __init__(self, budget_id, amount, amount_in_euro, name=None):
        self.id = budget_id
        self.amount = AdWordsService.euro_to_micro(amount) if amount_in_euro else amount
        self.name = name or 'API Budget #{uuid}'.format(uuid=uuid.uuid4().int)
        assert self.amount >= 10000  # i.e. >= 1 cent

    def add_operation(self, delivery="ACCELERATED"):
        """ Add operation for AdWords API"""
        operation = {
            "xsi_type": "BudgetOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "Budget",
                "name": self.name,
                "budgetId": self.id,
                "amount": {
                    "microAmount": self.amount
                },
                "deliveryMethod": delivery,
                "isExplicitlyShared": "false"
            }
        }
        return operation
