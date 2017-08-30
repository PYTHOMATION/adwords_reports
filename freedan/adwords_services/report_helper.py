import itertools
import pandas as pd

from freedan.adwords_services.adwords_service import AdWordsService

SPECIAL_FLOATS = (pd.np.inf, -pd.np.inf, pd.np.nan)


def convert_adwords_columns(df, add_operation_type=True, remove_pluses=True):
    """ Normalise/Add some often used columns in AdWords Reports
    :param df: DataFrame, normally a report downloaded from AdWords API
    :param add_operation_type: bool, needed for Device Multipliers, since the operation type changes depending
                                     whether a modifier is already available or not
    :param remove_pluses: bool, if True: Remove pluses from broad modified keywords in Criteria column
    :return: DataFrame
    """
    micro_columns = ("CpcBid", "Cost")
    share_columns = ("SearchRankLostImpressionShare", )
    upper_columns = ("KeywordMatchType", )
    criteria_columns = ("Criteria", )

    cols_to_func = {
        micro_columns: micro_to_float,
        share_columns: share_to_float,
        upper_columns: str.upper,
        criteria_columns: lambda x: criteria_cleaning(x, remove_pluses)
    }

    obj_dev_combos = itertools.product(["AdGroup", "Campaign"], ["Desktop", "Mobile", "Tablet"])
    modifier_columns = ["{obj}{dev}BidModifier".format(obj=obj, dev=dev) for obj, dev in obj_dev_combos]

    for col in df.columns:
        for col_group, func in cols_to_func.items():
            if col in col_group:
                df[col] = df[col].apply(func)

        if col in modifier_columns:
            if add_operation_type:
                op_type_col = col.replace("BidModifier", "_OperationType")
                df[op_type_col] = df[col].apply(operation_type)
            df[col] = df[col].apply(modifiers_to_float)
    return df


def micro_to_float(micro_amount, default_value=-1.00):
    """ Convert micro amounts to regular euro with default value if unexpected value occurs """
    try:
        return AdWordsService.micro_to_reg(micro_amount)
    except ValueError:
        return default_value


def share_to_float(share, default_value=-1.00):
    """ Convert str values representing impression share to actual numbers """
    if share == " --":
        return default_value
    elif share == "> 90%":
        return 0.9
    else:
        return float(share[:-1]) / 100.0


def modifiers_to_float(value):
    """ Convert str values representing device modifiers to actual numbers """
    try:
        return (float(value[:-1]) / 100.0) + 1
    except ValueError:
        return 1.0


def operation_type(raw_modifier):
    """ Determine if later on an ADD or SET operation needs to be send to AdWords API
    ' --' represents a non-existing device modifier -> ADD operation.
    else 'SET'
    """
    if "--" in raw_modifier:
        return "ADD"
    else:
        return "SET"


def criteria_cleaning(text, remove_pluses):
    text = text.lower()
    if remove_pluses:
        text = text.replace("+", "")
    return text


def replace_special_float(obj, new_value=0.0, special_values=SPECIAL_FLOATS):
    """ Replace special values like np.nan or np.inf.
    Needed when calculating rates like CTR directly (division by 0 may occur)
    """
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        return obj.replace(special_values, new_value)
    elif isinstance(obj, float):
        return new_value if obj in special_values else obj
