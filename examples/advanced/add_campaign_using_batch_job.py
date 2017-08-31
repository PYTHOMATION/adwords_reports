import freedan
from freedan import CampaignBudget, Campaign, AdGroup, Keyword, ExtendedTextAd


def add_adgroup_using_batch_job(path_credentials, is_debug):
    """
    A script that will add an adgroup with keywords and ads using batch upload.

    :param path_credentials: str, path to your adwords credentials file
    :param is_debug: bool
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        # define new adwords instances.
        # of course you can add multiple adgroups per campaign and multiple keywords/ads per adgroup.
        # check out add_adgroup_using_batch_job.py for more details
        budget = CampaignBudget(amount=10)
        campaign = Campaign(name="test_campaign_1")
        adgroup = AdGroup(name="test_adgroup_1")
        keyword = Keyword(text="asofjna", match_type="EXACT", bid=1.0, final_url="https://aiosjda.de")
        ad = ExtendedTextAd(headline1="yo", headline2="yoyo", description="dem boys",
                            path1="Yo", path2="Dude", final_url="https://aiosjda.de")

        # determine temporary ids for batch upload
        # magic: those ids are different from another ;)
        temp_id_helper = freedan.TempIdHelper()
        budget_id = temp_id_helper.temp_id
        campaign_id = temp_id_helper.temp_id
        adgroup_id = temp_id_helper.temp_id

        # operations
        budget_operations = [budget.add_operation(temp_id=budget_id)]
        campaign_operations = [campaign.add_operation(budget_id=budget_id, campaign_id=campaign_id)]
        # you might need additional operations for device, language or location targetings based on your business logic

        adgroup_operations = [adgroup.add_operation(campaign_id=campaign_id, bid=0.01, adgroup_id=adgroup_id)]
        keyword_operations = [keyword.add_operation(adgroup_id=adgroup_id)]
        ad_operations = [ad.add_operation(adgroup_id=adgroup_id)]

        # upload
        operations = (budget_operations, campaign_operations, adgroup_operations, keyword_operations, ad_operations)
        adwords_service.upload(operations, is_debug=is_debug, method="batch")


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    add_adgroup_using_batch_job(adwords_credentials_path, is_debug=True)
