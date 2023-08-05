#!/usr/bin/env python
# coding: utf-8

# Developer: Carlos Hernandez (cseHdz)
# Date: October 2018

# User defined
from dextract.helpers import clean

# Packages
import pandas as pd

# In[]
def __pop_level(lv_obj, lv_value, depth, lv_names = {}):

    """ Add dictionary keys as columns in dataframes
        Recursively explore keys in a dictionary

        lv_obj refers to the object at the current depth
        lv_names is a dictionary of names given (lv_value, depth) combinations

        If a string or None is found, return error String

        For single Dataframes - add columns
        For lists - iterate numerically
        For dictionary - pop lv_obj by lv_obj
    """

    """ Get the name for the current column """
    if isinstance(lv_names, dict) and len(lv_names) > 0:
        lv_name = lv_names.get((lv_value, depth), str(depth) + 'L')
    else: lv_name = str(depth) + 'L'

    # print(lv_value, depth, type(lv_obj), lv_name)

    if lv_obj is None: return str(lv_name) + ' - Not Found'
    elif isinstance(lv_obj, str): return  lv_name + " - " + lv_obj

    elif isinstance(lv_obj, pd.DataFrame): # Single Dataframe

        result = lv_obj
        """ Add a table ID to identify source """
        if 'ID' in result.columns:
            result['ID'] = str(lv_value) + '-' + result['ID']
        else: result['ID'] = str(lv_value)

        result = clean.clean_df(lv_obj, add_columns = {lv_name: lv_value})

        return result

    elif isinstance(lv_obj, list):

        """ Add this level to all the members of the list
            List is a passthrough for all objects at the current level
        """
        result = []
        for obj in lv_obj:
            temp = __pop_level(obj, lv_value, depth, lv_names = lv_names)

            """ Extend a list, Pop a dictionary, or append Dataframe """
            if isinstance(temp, list): result.extend(temp)
            else: result.append(temp)

        return result

    elif isinstance(lv_obj, dict):

        """ Pop the current level of a dictionary
            Dive a level deeper
        """
        result = []
        for key, obj in lv_obj.items():
            temp = __pop_level(obj, key, depth + 1, lv_names)
            if isinstance(temp, list):
                result.extend(__pop_level(temp, lv_value, depth, lv_names))
            else: result.append(temp)
        return result


# In[]
def pop_keys_df_dict(df_dict, dict_name = 'Output' , **kwargs):

    #print('Pop Keys - ', kwargs, df_dict.keys())
    """ Trigger recurve process to convert dict kets to cdf columns """
    lv_names = kwargs.get("lv_names", {})
    result = __pop_level(df_dict, dict_name, 0, lv_names)

    """ Transform list into dictionary
        - get name from a specific column
        - get name from explicit dictionary matching joined levels
        - get name from ordered list
    """
    if kwargs.get("name_from_list") is not None:
        name_list = kwargs.get("name_from_list")

        if len(name_list) == len(result):
            return {name: r for r in result for name in name_list}

    elif kwargs.get("name_from_dictionary") is not None:

        name_dict = kwargs.get("name_from_dictionary")
        new_dict ={'errors':[], } # Restart the dictionary

        for item in result:
            if isinstance(item, pd.DataFrame) and 'ID' in item.columns\
            and len(item['ID'])> 0:

                """ Find name in dictionary or label as unkown, ensure names
                    are unique """
                name = name_dict.get(item['ID'].iloc[0], "Unknown")
                count = int(sum([1 if name == n else 0 \
                                 for n in new_dict.keys()]) or 0)
                name = name if count == 0 else name + '_' + str(count + 1)
                new_dict[name] = item

            else: new_dict['errors'].append(item)

        return new_dict

    else: return result
