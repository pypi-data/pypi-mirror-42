#!/usr/bin/env python
# coding: utf-8

# Developer: Carlos Hernandez (cseHdz)
# Date: October 2018

""" ----------------------------- IMPORTING --------------------------------"""
# In[]:
#User defined methods
from dextract.helpers import clean

# Packages
import os
import xlrd
import pyexcel as pe
import pyexcel_xls
import pyexcel_xlsx

"""
Optional Parameters
-----------

XL Extraction:
------------------------- Extracting XL Files --------------------------------
- parallel_xl (int):
    Outline the number of parallel processes to run

- process (dict): data process to follow (includes all sections below)
    requires extraction, pre_clean and post_clean keys

- as_named_list (Bool):
    Transform the result from extraction into a named list

- names_from_list (list):
    list of names to use for name_list

- names_from_dict {df['ID']: name}:
    dictionary of names to assigned depending on the ID column
    generated through conversion to list
---------------------- Extracting Individual Shets Files ----------------------

- unmerge (bool):
    Unmergecells identified as merged in xlrd

"""

# In[]:
def data_from_xl(path, file_name, sheets, unmerge = True, **kwargs):

    # print('Xl - ', kwargs)

    """ Process an excel from list of sheets provided.
    """
    result = {s: data_from_xl_sheet(path, file_name, s,
                                    unmerge, **kwargs) for s in sheets}

    return result


# In[]:
def data_from_xl_sheet(path, file_name, sheet_name, unmerge = True, **kwargs):

    """ Extract an Excel Sheet using available parameters
        - xlrd is used for unmerging
        - pyexcel is used otherwise
    """

    full_path = os.path.join(path, file_name)

    try:
        data = __unmerge_xl(full_path, sheet_name) if unmerge \
        else pe.get_array(file_name = full_path, sheet_name = sheet_name)
    except:
        return sheet_name + ' - Not Found'

    data = clean.clean_data(data, trim_strings = True)

    return data


# In[]:
def data_from_csv (path, file_name, **kwargs):

    """ Extract a csv using available parameters
    """
    data = pe.get_array(file_name = os.path.join(path, file_name),
                        encoding = 'utf-8-sig')

    data = clean.clean_data(data, trim_strings = True)

    return data


""" -----------------------------EXCEL HELPERS------------------------------"""
# In[]:
def __unmerge_xl(full_path, sheet_name):

    """ Unmerge cells in a workbook """
    xl = xlrd.open_workbook(full_path, on_demand = True)
    sheet = xl.sheet_by_name(sheet_name)

    """ Intialize data as a list of lists """
    data = [sheet.row_values(i) for i in range(0, sheet.nrows)]

    """ Copy files from merged cells """
    for rs, re, cs, ce in sheet.merged_cells:
        for row in range(rs, re):
            for col in range(cs, ce):
                data[row][col] = data [rs][cs]
    return data
