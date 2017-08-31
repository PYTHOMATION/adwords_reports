import freedan
from freedan import AdGroup, Keyword, ExtendedTextAd


CAMPAIGN_ID = "INSERT_ID_HERE"


def add_adgroup_using_batch_job(path_credentials, is_debug):
    """
    A script that will add an adgroup with keywords and ads using batch upload.

    :param path_credentials: str, path to your adwords credentials file
    :param is_debug: bool
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        # define new adwords instances
        adgroup = AdGroup(name="test_adgroup_1")
        keyword1 = Keyword(text="asofjna", match_type="EXACT", bid=1.0, final_url="https://aiosjda.de")
        keyword2 = Keyword(text="asofjna", match_type="PHRASE", bid=0.5, final_url="https://aiosjda.de")
        ad1 = ExtendedTextAd(headline1="yo", headline2="yoyo", description="dem boys",
                             path1="Yo", path2="Dude", final_url="https://aiosjda.de")
        ad2 = ExtendedTextAd(headline1="yo", headline2="yoyo", description="dem boyoyoyoys",
                             path1="Yo", path2="Dude", final_url="https://aiosjda.de")

        # determine temporary id for adgroup
        temp_id_helper = freedan.TempIdHelper()
        adgroup_id = temp_id_helper.temp_id

        # operations
        adgroup_operations = [adgroup.add_operation(campaign_id=CAMPAIGN_ID, bid=0.01, adgroup_id=adgroup_id)]
        keyword_operations = [
            keyword1.add_operation(adgroup_id=adgroup_id),
            keyword2.add_operation(adgroup_id=adgroup_id)
        ]
        ad_operations = [
            ad1.add_operation(adgroup_id=adgroup_id),
            ad2.add_operation(adgroup_id=adgroup_id)
        ]

        # upload
        operations = (adgroup_operations, keyword_operations, ad_operations)
        adwords_service.upload(operations, is_debug=is_debug, method="batch")


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    add_adgroup_using_batch_job(adwords_credentials_path, is_debug=True)
