import freedan
from freedan import Label


ADGROUP_ID = "INSERT_ID_HERE"
LABEL_TEXT = "INSERT_TEXT_HERE"


def label_adgroups(path_credentials, is_debug):
    """
    A script that will apply a label to an AdGroup.

    To apply a label to an AdGroup you need to create the label first. You might therefore encounter one of the
    following three scenarios:
        1. label exists and you know its ID (per account)
        2. label exists, but you don't know its ID
        3. label might exist, but you're not sure.
        4. label doesn't exist yet

    freedan provides a convenient interface for any of those.

    :param path_credentials: str, path to your adwords credentials file
    :param is_debug: bool
    """
    adwords_service = freedan.AdWordsService(path_credentials)
    for account in adwords_service.accounts():
        print(account)

        ag_label = Label(LABEL_TEXT, label_id=None)

        # in case 1: provide label_id in initiation and skip Label.update_id call
        # in other cases: adapt 'action_if_not_found' parameter to your needs

        ag_label.update_id(adwords_service, is_debug=is_debug, action_if_not_found="create")
        operations = [ag_label.apply_on_adgroup_operation(adgroup_id=ADGROUP_ID)]

        # upload will display an error if debug mode and label isn't existing yet
        adwords_service.upload(operations, is_debug=is_debug, method="standard")


if __name__ == "__main__":
    adwords_credentials_path = "adwords_credentials.yaml"
    label_adgroups(adwords_credentials_path, is_debug=True)
