import numpy as np


def list_dicts_to_dict_lists(lst: list):
    """convert list of dict to dict of lists"""
    dict_keys = lst[0].keys()
    return {key: [d.get(key, np.NaN) for d in lst] for key in dict_keys}
