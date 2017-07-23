from freedan.adwords_services.adwords_service import DEVICE_TO_ID


class Campaign:
    """ Campaigns contain AdGroups
    In our accounts they usually group together routes by route types, population sizes and main keyword
    """
    def __init__(self, name):
        self.name = name

    def add_operation(self, budget_id, campaign_id=None, status="ENABLED"):
        """ Campaign add operation for AdWords API """
        operation = {
            "xsi_type": "CampaignOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "Campaign",
                "name": self.name,
                "id": campaign_id,
                "status": status,
                "advertisingChannelType": "SEARCH",
                "adServingOptimizationStatus": "ROTATE",
                "budget": {
                    "budgetId": budget_id
                },
                "biddingStrategyConfiguration": {
                    "biddingStrategyType": "MANUAL_CPC"
                },
                "settings": [{
                        "xsi_type": "GeoTargetTypeSetting",
                        "positiveGeoTargetType": "LOCATION_OF_PRESENCE",
                        "negativeGeoTargetType": "LOCATION_OF_PRESENCE"
                }],
                "networkSetting": {
                    "targetGoogleSearch": "true",
                    "targetSearchNetwork": "false",
                    "targetContentNetwork": "false",
                    "targetPartnerSearchNetwork": "false"
                }
            }
        }
        return operation

    @staticmethod
    def delete_operation(campaign_id):
        """ Campaign delete operation for AdWords API """
        operation = {
            "xsi_type": "CampaignOperation",
            "operator": "SET",
            "operand": {
                "xsi_type": "Campaign",
                "id": campaign_id,
                "status": "REMOVED"
            }
        }
        return operation

    @staticmethod
    def set_language(campaign_id, language_id, operator="ADD"):
        """ Set a language targeting on a campaign
        Check language ids at
        """
        operation = {
            "xsi_type": "CampaignCriterionOperation",
            "operator": operator,
            "operand": {
                "xsi_type": "CampaignCriterion",
                "campaignId": campaign_id,
                "criterion": {
                    "xsi_type": "Language",
                    "id": language_id
                }
            }
        }
        return operation

    @staticmethod
    def set_device_modifier(campaign_id, multiplier, device_type, operator="SET"):
        """ Set a device multiplier on a campaign """
        operation = {
            "xsi_type": "CampaignCriterionOperation",
            "operator": operator,
            "operand": {
                "xsi_type": "CampaignCriterion",
                "campaignId": campaign_id,
                "criterion": {
                    "xsi_type": "Platform",
                    "id": DEVICE_TO_ID[device_type]
                },
                "bidModifier": multiplier,
            }
        }
        return operation

    @staticmethod
    def set_pos_location_modifier(campaign_id, multiplier, location_id, operator="ADD"):
        """ Set a positive location targeting on a campaign """
        operation = {
            "xsi_type": "CampaignCriterionOperation",
            "operator": operator,
            "operand": {
                "xsi_type": "CampaignCriterion",
                "campaignId": campaign_id,
                "criterion": {
                    "xsi_type": "Location",
                    "id": location_id
                },
                "bidModifier": multiplier,
            }
        }
        return operation

    @staticmethod
    def set_neg_location_modifier(campaign_id, location_id, operator="ADD"):
        """ Block a location targeting on a campaign """
        operation = {
            "xsi_type": "CampaignCriterionOperation",
            "operator": operator,
            "operand": {
                "xsi_type": "NegativeCampaignCriterion",
                "campaignId": campaign_id,
                "criterion": {
                    "xsi_type": "Location",
                    "id": location_id
                }
            }
        }
        return operation

    @staticmethod
    def set_name_operation(campaign_id, new_name):
        """ Change name operation of campaign """
        operation = {
            "xsi_type": "CampaignOperation",
            "operator": "SET",
            "operand": {
                "xsi_type": "Campaign",
                "id": campaign_id,
                "name": new_name
            }
        }
        return operation

    @staticmethod
    def shared_set_operation(operation_type, campaign_id, shared_set_id):
        """ Apply/Remove a shared set operation of campaign """
        assert operation_type in ["ADD", "REMOVE"]

        operation = {
            "xsi_type": "CampaignSharedSetOperation",
            "operator": operation_type,
            "operand": {
                "campaignId": campaign_id,
                "sharedSetId": shared_set_id
            }
        }
        return operation

    @staticmethod
    def apply_shared_set(campaign_id, shared_set_id):
        """ Apply a shared set operation of campaign """
        return Campaign.shared_set_operation("ADD", campaign_id, shared_set_id)

    @staticmethod
    def remove_shared_set(campaign_id, shared_set_id):
        """ Remove a shared set operation of campaign """
        return Campaign.shared_set_operation("REMOVE", campaign_id, shared_set_id)

    @staticmethod
    def apply_user_list(campaign_id, user_list_id, multiplier):
        """ Apply a shared set operation of campaign """
        operation = {
            "xsi_type": "CampaignCriterionOperation",
            "operator": "ADD",
            "operand": {
                "xsi_type": "CampaignCriterion",
                "campaignId": campaign_id,
                "criterion": {
                    "xsi_type": "CriterionUserList",
                    "userListId": user_list_id
                },
                "bidModifier": multiplier,
            }
        }
        return operation

    def __repr__(self):
        """ user friendly string representation of campaign """
        return self.name
