def test_add_budget(capfd):
    from tests import adwords_service, no_error_stdout
    from freedan import CampaignBudget

    budget = CampaignBudget(amount=200, convert_to_micro=True)
    operations = [budget.add_operation(temp_id=-1)]

    adwords_service.upload(operations, is_debug=True, service_name="BudgetService")

    out, err = capfd.readouterr()
    assert out == no_error_stdout

