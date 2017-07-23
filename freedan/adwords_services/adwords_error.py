class AdWordsError:
    """ AdWords service class that takes care of elegant error handling. """
    def __init__(self, index, error_type, trigger, sub_type, field_path, reason,
                 policy_name, policy_violating_text, feed_name, feed_attribute_name):
        self.index = index  # to trace back the operation

        self.type = error_type
        self.trigger = trigger
        self.sub_type = sub_type
        self.field_path = field_path
        self.reason = reason

        # PolicyViolationError
        self.policy_name = policy_name
        self.policy_violating_text = policy_violating_text

        # FeedAttributeReferenceError
        self.feed_name = feed_name
        self.feed_attribute_name = feed_attribute_name

    @classmethod
    def from_adwords_error(cls, index, adwords_error):
        """ Create from internal adwords error object
        :param index: int, index in operations list
        :param adwords_error: internal adwords error object (dict like) 
        :return: AdWordsError instance
        """
        index = int(index)
        print(index)
        print(adwords_error)
        print("*" * 130)

        # mandatory fields
        error_type = adwords_error["ApiError.Type"]
        trigger = adwords_error["trigger"]
        sub_type = adwords_error["errorString"]
        field_path = adwords_error["fieldPath"]

        # optional fields
        reason = adwords_error["reason"] if "reason" in adwords_error else None
        feed_name = adwords_error["feedName"] if "feedName" in adwords_error else None
        feed_attribute_name = adwords_error["feedAttributeName"] if "feedAttributeName" in adwords_error else None

        if error_type == "PolicyViolationError":
            policy_name = adwords_error["key"]["policyName"]
            policy_violating_text = adwords_error["key"]["violatingText"]
        else:
            policy_name = None
            policy_violating_text = None

        return cls(index=index, error_type=error_type, trigger=trigger, sub_type=sub_type, field_path=field_path,
                   reason=reason, policy_name=policy_name, policy_violating_text=policy_violating_text,
                   feed_name=feed_name, feed_attribute_name=feed_attribute_name)

    def to_string(self):
        """ Easy to read output for user feedback """
        internal_attributes = ["index"]

        error_info_text = ["Operation {index} - FAILURE:".format(index=self.index)]
        error_info_text += ["\t{field}={error}".format(field=field, error=value)
                            for field, value in vars(self).items() if value and (field not in internal_attributes)]
        return "\n".join(error_info_text)

    def __repr__(self):
        return self.to_string()

