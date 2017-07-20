from src.models.adwords import (MAX_CHARS_HEADLINE1, MAX_CHARS_HEADLINE2, MAX_CHARS_DESCRIPTION,
                                MAX_CHARS_PATH1, MAX_CHARS_PATH2)

from freedan.other_services.text_handler import TextHandler


class ExtendedTextAd:
    """ Common functionality needed for Ad creation/validation/deletion/etc. """
    def __init__(self, headline1, headline2, description, path1, path2, final_url):
        path1, path2 = self.clean_paths(path1, path2)

        self.headline1 = headline1
        self.headline2 = headline2
        self.description = description
        self.path1 = path1
        self.path2 = path2
        self.final_url = final_url

    @staticmethod
    def clean_paths(path1, path2):
        """ Remove punctuation and spaces from paths """
        path1, path2 = TextHandler.remove_punctuation([path1, path2])
        path1 = path1.replace(" ", "")
        path2 = path2.replace(" ", "")
        return path1, path2

    def too_long(self):
        """ Determine whether an Ad could be uploaded to AdWords or if it's too long """
        boundaries = {
            self.headline1: MAX_CHARS_HEADLINE1,
            self.headline2: MAX_CHARS_HEADLINE2,
            self.description: MAX_CHARS_DESCRIPTION,
            self.path1: MAX_CHARS_PATH1,
            self.path2: MAX_CHARS_PATH2
        }

        for field, max_length in boundaries.items():
            if len(field) > max_length and "{=" not in field:
                # "{=" means that special functions of adwords are used where more characters can be used
                # this function could be more specific but it's sufficient for now
                return True
        return False

    def basic_checks(self):
        """ basic condition that assert the ad is ready to be uploaded to AdWords """
        assert self.headline1
        assert self.headline2
        assert self.description
        assert self.path1 if self.path2 else True
        assert all(" " not in path for path in [self.path1, self.path2])  # no spaces in path
        assert "https://" in self.final_url
        assert not self.too_long()

    def add_operation(self, adgroup_id, status="ENABLED"):
        """ Ad add operation for AdWords API.
        Only working for ETA since Standard Text Ads were deprecated in early 2017
        """
        self.basic_checks()

        operation = {
            "xsi_type": "AdGroupAdOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "AdGroupAd",
                "adGroupId": adgroup_id,
                "status": status,
                "ad": {
                    "xsi_type": "ExpandedTextAd",
                    "headlinePart1": self.headline1,
                    "headlinePart2": self.headline2,
                    "description": self.description,
                    "path1": self.path1,
                    "path2": self.path2,
                    "finalUrls": [self.final_url]
                }
            }
        }
        return operation

    @staticmethod
    def pause_operation(adgroup_id, ad_id):
        """ Ad pause operation for AdWords API """
        operation = {
            "operator": "SET",
            "xsi_type": "AdGroupAdOperation",
            "operand": {
                "adGroupId": adgroup_id,
                "ad": {
                    "id": ad_id,
                },
                "status": "PAUSED"
            }
        }
        return operation

    @staticmethod
    def delete_operation(adgroup_id, ad_id):
        """ Ad delete operation for AdWords API """
        operation = {
            "operator": "REMOVE",
            "xsi_type": "AdGroupAdOperation",
            "operand": {
                "xsi_type": "AdGroupAd",
                "adGroupId": adgroup_id,
                "ad": {
                    "id": ad_id
                }
            }
        }
        return operation

    def __repr__(self):
        """ user friendly string representation of an ad """
        repr_message = "{h1}\n{h2}\n{desc}\n{p1}\n{p2}\n{final_url}".format(
            h1=self.headline1, h2=self.headline2, desc=self.description,
            p1=self.path1, p2=self.path2, final_url=self.final_url)
        return repr_message
