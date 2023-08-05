
#!/usr/bin/env python
# coding: utf-8

# Developer: Carlos Hernandez (cseHdz)
# Date: October 2018

# In[]:

# Packages
import copy
import pandas as pd
import numpy as np

from collections import OrderedDict
from itertools import repeat
"""
Pre_Clean:
----------------------------- Pre-Cleaning Process ----------------------------

- trim_strings(Bool)
Trim all strings in a df

- transpose_data (Bool):
    Transpose rows to cols

- ignore_empty_rows (Bool):
    Delete fully empty rows

- ignore_empty_cols (Bool):
    Delete fully empty cols

- ignore_empty_cells (Bool):
    Ignore non-complete rows

- delete_by_threshold (float 0-1)
    Filter rows that are empty to a certain threshold


Post_Clean:
----------------------------- Post-Cleaning Process ---------------------------

- treat_axis_as_data (axis):
    Treat entire axis as data type

- header_row (int):
    Arbitrary header row

- header_column (int):
    Arbitrary header column

- fill_headings (Bool):
    Fill columns and rows identified as HEADING (ffill)

- index_as_col (Bool):
    Add index as a column

- compress_header (Bool):
    Unique value for columns based on index HEADINGS

- add_header (df):
    Custom header to append to the result df(s)

- ensure_no_rep (list or str)
    Ensure values are not repeated in a series

- transpose_output (Bool):
    Transpose final df

- drop_partial_records (Bool):
    Remove records that are incomplete

- drop_empty_records (Bool):
    Remove records that are fully empty

- drop_empty_columns (Bool):
    Remove columns that are fully empty

- add_columns {name: default_value}:
    Add columns with a specified name and a default value

- columns_as_row (Bool):
    Add columns as Header

- rename_columns {cur_name: new_name}:
    Rename columns in a dataframe

- rename_index {cur_name: new_name}:
    Rename rows in a dataframe

- delete_rows ([name_list])
    Delete a list of columns if found

- delete_columns ([name_list])
    Delete a list of columns if found

- delete_escape_chars (Bool)
    Delete all escape chars

- del_cols_by_threshold (Double)
    Delete cols that are empty by threshold

- del_rows_by_threshold(Double)
    Delete rows that are empty by threshold

"""

# In[]:
def clean_data(data, **kwargs):

    #print('Pre Clean - ', kwargs)

    """ Trim data """
    if kwargs.get("trim_strings", False):
        data = __trim_strings(data)

    """ Transpose data priorng """
    if kwargs.get("transpose_data", False):
        data = __transpose_data(data)

    """ Ignore all rows that are completely empty """
    if kwargs.get("ignore_empty_rows", False):
        data = __delete_empty_rows(data)

    """ Ignore all rows that are completely empty """
    if kwargs.get("ignore_empty_cols", False):
        data = __delete_empty_cols(data)

    """ Ignore any row with at least one empty column """
    if kwargs.get("ignore_empty_cells", False):
        data = __delete_empty_cells(data)

    """ Ignore any row with empty columns as per threshold """
    if kwargs.get("delete_by_threshold") is not None:
        data = __delete_by_threshold(data, kwargs.get("delete_by_threshold"))

    return data

# In[]:
def clean_df(df, **kwargs):

    #print('Post Clean - ', kwargs)
    if not isinstance(df, pd.DataFrame):
        return df

    """ Treat all entries in axis as data"""
    if kwargs.get("treat_axis_as_data") is not None:
        axis = kwargs.get("treat_axis_as_data")
        if axis == 'both':
            df = __treat_axis_as_data(df, 'columns')
            axis = 'rows'
        df = __treat_axis_as_data(df, axis)

    """ Add the current Index as a Row - Sensitive to positioning """
    if kwargs.get("index_as_col", False):
        df = __add_index_as_col(df)

    """ Identify an arbitrary header row """
    if kwargs.get("header_row") is not None:
        header_row = kwargs.get("header_row", False)
        if header_row >= 0 and header_row <= df.shape[0] -1:
            df = __rename_df(df, {df.iloc[header_row].name:'fH'}, axis = 0)

    """ Identify an arbitrary header column """
    if kwargs.get("header_column") is not None:
        header_column = kwargs.get("header_column", False)
        if header_column >= 0 and header_column <= df.shape[1] -1:
            df = __rename_df(df, {list(df.columns)[header_column]:'fH'},
                                  axis = 1)

    """ Fill records and columns qualified as Headings """
    if kwargs.get("fill_headings", False):
        df = __fill_headings(df)

    """ Compress Headings to values from rows """
    if kwargs.get("compress_header", False):
        df = __compress_header(df)

        """ Add the current Index as a Row - Sensitive to positioning """
    if kwargs.get("columns_as_row", False):
        df = __add_columns_as_row(df)

    """ Compress Headings to values from rows """
    if kwargs.get("add_header") is not None:
        df = __add_header_to_df(df, kwargs.get("add_header"))

    """ Ensure there are no repetitions in a pandas series """
    if kwargs.get("ensure_no_rep") is not None:
        rows_to_check = kwargs.get("ensure_no_rep")
        if isinstance(rows_to_check, list):
            for r in rows_to_check:
                if r in df.index: df.loc[r] = __ensure_no_rep(df.loc[r])
        elif isinstance(rows_to_check, str) and rows_to_check in df.index:
            df.loc[rows_to_check] = __ensure_no_rep(df.loc[rows_to_check])

    """ If partial records should be deleted """;
    if kwargs.get("drop_partial_records", False):
        df = __drop_empty_records(df, 'any')

    """ If full empty records should be deleted """
    if kwargs.get("drop_empty_records", False):
        df = __drop_empty_records(df, 'all')

    """ If full empty columns should be deleted """
    if kwargs.get("drop_empty_columns", False):
        df = __drop_empty_columns(df)

    """ Transpose the df """
    if kwargs.get("transpose_output", False):
        df = __transpose_df(df)

    """ Add columns to the dataset """
    if kwargs.get("add_columns") is not None:
        cols_dict = kwargs.get("add_columns")
        if isinstance(cols_dict, dict):
            df = __add_columns_to_df(df, cols_dict)

    """ Rename with Headers """
    if kwargs.get("rename_columns") is not None:
        new_names = kwargs.get("rename_columns")
        if isinstance(new_names, dict):
            df = __rename_df(df, new_names, axis = 1)

    """ Rename Indices """
    if kwargs.get("rename_index") is not None:
        new_names = kwargs.get("rename_index")
        if isinstance(new_names, dict):
            df = __rename_df(df, new_names, axis = 0)

    """ Delete a list columns """
    if kwargs.get("delete_columns") is not None:
        col_list = kwargs.get("delete_columns")
        if isinstance(col_list, list):
            df = __del_from_df(df, col_list, axis = 1)

    """ Delete a list columns """
    if kwargs.get("delete_rows") is not None:
        row_list = kwargs.get("delete_rows")
        if isinstance(row_list, list):
            df = __del_from_df(df, row_list, axis = 0)

    """ Delete Escape Chars """
    if kwargs.get("delete_escape_chars", False):
            df = __del_escape_chars_df(df)

    """ Delete columns that are empty up to a threshold """
    if kwargs.get("del_cols_by_threshold") is not None:
        threshold = kwargs.get("del_cols_by_threshold")
        df = __delete_by_threshold_df(df, threshold, axis = 'columns')

    """ Delete rows that are empty up to a threshold """
    if kwargs.get("del_rows_by_threshold") is not None:
        threshold = kwargs.get("del_rows_by_threshold")
        df = __delete_by_threshold_df(df, threshold, axis = 'index')

    return df


""" ---------------------------- DATA FUNCTIONS ----------------------------"""
# In[]:
def __trim_strings(data):

    """ Trim all strings within each row """
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if isinstance(data[r][c], str): data[r][c] = data[r][c].strip()

    return data

# In[]:
def __transpose_data(data):

    """ Transpose a list of lists """
    return np.transpose(data).tolist()


# In[]:
def __filter_row(row, f_string, partial = False):

    """ Filter rows that contain f_string, either all or partial(any) flags """
    n = sum([1 if x != f_string else 0 for x in row])
    if partial: return n
    return n == 0


# In []:
def __delete_empty_rows(data):
    """ Filter rows that are empty """
    return [r for r in data if not(__filter_row(r, ''))]


# In[]:
def __delete_empty_cols(data):

    """ Filter columns that are empty (transpose and process as columns) """
    temp = __delete_empty_rows(__transpose_data(data))
    return __transpose_data(temp)


# In []:
def __delete_empty_cells(data):

    """ Filter rows that are empty """
    return [r for r in data if __filter_row(r, '', partial = True) == len(r)]


# In []:
def __delete_by_threshold(data, threshold):

    """ Filter rows that are empty to a certain threshold """
    return [r for r in data if __filter_row(r, '', partial = True) >= \
            (1-threshold) * len(r)]

"""--------------------------- Data Frame Helpers --------------------------"""

def __treat_axis_as_data(df, axis):

    """ Determe axis to use for headings """
    headings = df.columns if axis == 1 or axis == 'columns' else df.index

    """ If not currently labelled as DATA, add D subscript """
    new_names = {h: str(h) + 'D' for h in headings if str(h)[-1] != 'D'}
    df = __rename_df(df, new_names = new_names, axis = axis)

    return df


# In[]:
def __drop_empty_records(df, how = 'all'):

    """ Replace spaces and empty characters with np.nan """
    result = df.replace(r"^(?![\s\S])|^(\s)", np.nan,
                   regex = True).dropna(how = how)
    result = result.replace(np.nan, '')
    return result


def __drop_empty_columns(df):

    """ Get a list of unique values and delete if all empty """
    cols = [col for col in df.columns if list(set(df[col])) == ['']]

    df = df.drop(columns= cols)
    return df


# In[]:
def __add_header_to_df(df, add_header):

    """ Extract the current record types """
    h_index = [x for x in df.index if str(x)[-1] != 'D']
    d_index = [x for x in df.index if str(x)[-1] == 'D']

    """ Add a header on top of rows """
    add_header.index = [str(i) + 'aH' for i in range(add_header.shape[0])]

    if len(h_index) > 0:
        header = pd.concat([df.loc[h_index], add_header], sort = False)
    else: header = add_header

    return pd.concat([header, df.loc[d_index]], sort = False)


# In[]:
def __add_columns_to_df(df, cols_dict):

    """ Add columns from a dictionary in the format
        cols_dict = {col_name : default_value} """
    result = copy.deepcopy(df)

    for name, value in cols_dict.items():
        result[name] = value

    return result


def __del_from_df(df, name_list, axis = 1):

    if axis == 'columns': axis = 1
    elif axis == 'index': axis = 0

    headings = df.columns if axis == 1 or axis == 'columns' else df.index

    """ Drop named rows/columns from a list """
    result = copy.deepcopy(df)

    for name in name_list:
        if name in headings:
            result.drop(name, axis  = axis, inplace = True)

    return result

# In[]:
def __add_index_as_col(df):

    """ Extract the Index from df """
    temp = pd.DataFrame(df.index)
    temp.index = df.index
    temp.columns = ['iH']

    return pd.concat([temp, df], axis = 1)


# In[]:
def __add_columns_as_row(df):

    """ Extract Columns from df """
    temp = pd.DataFrame(df.columns).T
    temp.columns = df.columns
    temp.index = ['iH']

    return pd.concat([temp, df], axis = 0)


# In[]:
def __fill_headings(df):

    """ Fill Columns & Rows identified as Headings """
    result = df
    for x in df.columns:
        if str(x)[-1] == 'H': result[x] = result[x].replace('', None)
    for x in df.index:
        if str(x)[-1] == 'H': result.loc[x] = result.loc[x].replace('', None)

    return result


# In[]:
def __rename_df(df, new_names = {}, axis = 1):


    """ Rename a DataFrame axis ensuring no repeated entries are found """
    names = {}

    """ Determe axis to use for headings """
    headings = df.columns if axis == 1 or axis == 'columns' else df.index

    for col in list(headings):
        """ If new_names is not specified, just ensure there is no
            repetition """
        key = new_names[col] if col in new_names.keys() else col
        if key == '': key = 'U' # Replace empty values with 'U' for Unknown

        key = str(key)
        """ Find the number of ocurrences and establish the new key """
        count = int(sum([1 if key == n else 0 \
                                 for n in names.values()]) or 0)

        new_key = key if count == 0 and len(key) > 1 else str(count + 1) + key

        """ Populate the dictionary of entries to be renamed"""
        names[col] = new_key

    result = df.rename(names, axis = axis)

    return result


# In[]:
def __compress_header(df):

    """ Identify Heading and Data Rows """
    h_index = [x for x in list(df.index) if str(x)[-1] == 'H']
    d_index = [x for x in list(df.index) if str(x)[-1] == 'D']

    """ If there is at least one heading - joing values of H rows """
    if len(h_index) > 0:
        header = df.loc[h_index]
        names = {}
        for k in df.columns:
            temp = list(OrderedDict(zip(header[k], repeat(None))))

            unique_vals = [x for x in temp if x not in [' ', '', '_']]
            if all(isinstance(h, str) for h in unique_vals):
                names[k] = '_'.join(unique_vals)

        result = __rename_df(df.loc[d_index], names, axis = "columns")
    else: result = df

    return result


# In[]:
def __transpose_df(df):

    """ Identify Heading and Data Rows """
    h_index = [x for x in list(df.index) if str(x)[-1] != 'D']
    d_index = [x for x in list(df.index) if str(x)[-1] == 'D']

    """ Identify Pivot Columns """
    v_index = [x for x in list(df.columns) if str(x)[-1] != 'D']

    """ Tranpose the data & the header """
    result = pd.melt(df.loc[d_index], id_vars = v_index)
    header = df.loc[h_index].T

    header = __del_escape_chars_df(header)

    """ Merge the header as columns, if repeated add '_y' to header columns """
    result = pd.merge(result, header, how = 'left', left_on ='variable',
                    right_index= True , suffixes = ('','_y'))

    """ Delete variable created by melt """
    result = result.drop(['variable'], axis = "columns")

    """ Attempt to find the proper headings - if exisiting
        (i.e. Pivot Columns) """
    if header.shape[0] > 0:

        names = {}
        for k in v_index:
            if k in header.index:
                temp = list(OrderedDict(zip(header.loc[k], repeat(None))))
                unique_vals = [x for x in temp if x not in [' ', '', '_']]

                if all(isinstance(h, str) for h in unique_vals if h ):
                    names[k] = '_'.join(unique_vals)

    if not(names is None):
        result = __rename_df(result, names, axis = "columns")

    return result

# In[]:
def __del_escape_chars_df(df):

    """ Replace escape characters with a space (' ') """
    escapes = ['\t', '\n', '\a', '\b', '\f', '\r', '\v']
    for e in escapes: df = df.replace(e, ' ', regex = True)

    return df


# In[]:
def __ensure_no_rep(series):

    """ Ensure there is no repetition in pandas Series """
    new_vals = []
    for index, value in series.iteritems():
        value = str(value)
        """ Find the number of ocurrences and establish the new value """
        count = int(sum([1 if value == v else 0 for v in new_vals]) or 0)
        new_val = value if count == 0 else value + str(count + 1)

        """ Add the new identified value """
        new_vals.append(new_val)
        series[index] = new_val

    return series


# In[]:
def __delete_by_threshold_df(df, threshold, axis = 'index'):

    if axis == 'columns': axis = 1
    elif axis == 'index': axis = 0

    result = df.replace(r"^(?![\s\S])|^(\s)", np.nan, regex = True)
    temp = result.count(axis = abs(axis-1))/result.shape[0]
    counts = temp[temp <= (1 - threshold)]
    for key in counts.keys():
        result = result.drop(key, axis=axis)

    result = result.replace(np.nan, '')

    return result
