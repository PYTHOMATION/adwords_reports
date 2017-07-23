import itertools
import pandas as pd

from freedan.adwords_services.adwords_service import AdWordsService

SPECIAL_FLOATS = (pd.np.inf, -pd.np.inf, pd.np.nan)


class ReportHelper:
    """ Centralizing some often used functionality for cleaning DataFrames/AdWords reports """
    def __init__(self):
        pass

    @staticmethod
    def replace_special_float(df, new_value=0.0, special_values=SPECIAL_FLOATS):
        """ Replace special values like np.nan or np.inf.
        Needed when calculating rates like VCR or CTR directly (vision by 0 may occur)
        """
        return df.replace(special_values, new_value)

    @classmethod
    def adwords_columns(cls, df, add_operation_type=True):
        """ Normalising/Adding some often used columns in AdWords Reports
        :param df: DataFrame, normally a report downloaded from AdWords API
        :param add_operation_type: bool, needed for Device Multipliers, since the operation type changes depending
                                         whether a modifier is already available or not
        :return: DataFrame
        """
        share_columns = ["SearchRankLostImpressionShare"]
        obj_dev_combos = itertools.product(["AdGroup", "Campaign"], ["Desktop", "Mobile", "Tablet"])
        modifier_columns = ["{obj}{dev}BidModifier".format(obj=obj, dev=dev) for obj, dev in obj_dev_combos]

        micro_columns = ["CpcBid", "Cost"]
        upper_columns = ["KeywordMatchType"]
        for col in df.columns:
            if col in modifier_columns:
                if add_operation_type:
                    ag_device_part = col.split("BidModifier")[0]
                    col_name = "{ag_device_part}_OperationType".format(ag_device_part=ag_device_part)
                    df[col_name] = cls.operation_type_from_raw_modifier(df[col])
                df[col] = cls.modifiers_to_float(df[col])

            if col in share_columns:
                df[col] = cls.shares_to_float(df[col])

            if col in micro_columns:
                df[col] = cls.micros_to_float(df[col])

            if col == "Criteria":
                df[col] = df[col].str.lower()\
                    .str.replace("+", "")

            if col in upper_columns:
                df[col] = df[col].str.upper()
        return df

    @classmethod
    def micros_to_float(cls, series):
        """ Convert micro amounts to regular euro for the whole column """
        return series.apply(cls.__micro_to_float)

    @classmethod
    def shares_to_float(cls, series):
        """ Convert str values representing impression share to actual numbers for whole column """
        return series.apply(cls.__share_to_float)

    @classmethod
    def modifiers_to_float(cls, series):
        """ Convert str values representing device modifiers to actual numbers for whole column """
        return series.apply(cls.__value_to_float)

    @classmethod
    def operation_type_from_raw_modifier(cls, series):
        """ Determine if later on an ADD or SET operation needs to be send to AdWords API """
        return series.apply(cls.__operation_type)

    @staticmethod
    def __micro_to_float(micro_amount, default_value=-1.00):
        """ Convert micro amounts to regular euro with default value if unexpected value occurs """
        try:
            return AdWordsService.micro_to_euro(micro_amount)
        except ValueError:
            return default_value

    @staticmethod
    def __share_to_float(share, default_value=-1.00):
        """ Convert str values representing impression share to actual numbers """
        if "--" in share:
            return default_value
        elif share == "> 90%":
            return 0.9
        else:
            return float(share[:-1]) / 100.0

    @staticmethod
    def __value_to_float(value):
        """ Convert str values representing device modifiers to actual numbers """
        try:
            return (float(value[:-1]) / 100.0) + 1
        except ValueError:
            return 1.0

    @staticmethod
    def __operation_type(raw_modifier):
        """ Determine if later on an ADD or SET operation needs to be send to AdWords API
        ' --' represents a non-existing device modifier -> ADD operation.
        else 'SET'
        """
        return "ADD" if "--" in raw_modifier else "SET"
