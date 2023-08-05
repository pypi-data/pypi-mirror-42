#!/usr/bin/env python
# coding: utf-8

# Developer: Carlos Hernandez (cseHdz)
# Date: October 2018

"""
Extraction:
--------------------------- Extraction Process --------------------------------
- data_loss (0-1):
    % of cells that must be empty to consider a cell empty

- thresholds {0: (0-1), 1: (0-1), 2:(0-1)}
    override statistic threshold generation

- method (str):
    slicing method

- s_output (str):
    Type of output to retrieve from slicing ([slice list], search, 'all')

- search_dict {name: search_str}:
    Values to find and name for resulting df

- concat_search_axis (int):
    Concatenate dfs if result from extraction is list
"""
# User defined
from dextract.helpers import clean

# Packages
import copy
import numpy as np
import pandas as pd
import statistics
from collections import Counter

# In[]:
def extract_slices(data, output = [0], **kwargs):

    # print('Extraction - ', kwargs)
    """ Extract data from a list of lists using a slicing method """
    if output not in ['all', 'search'] and not(isinstance(output, list)):
        return pd.DataFrame(data)

    df_slices = create_df_slices(data, **kwargs)

    if output == 'all':
        result = df_slices # Return everything - No Names
    elif output == 'search':
        result = map_slices(df_slices, **kwargs) # Return a named dictionary
    elif isinstance(output, list):
        result = [df_slices[i] for i in output if isinstance(i, int)]
    else: result = pd.DataFrame(data)

    """ Ensure return type is can be df, dict or list """
    return result


# In[]:
def map_slices(df_slices, search_dict, concat_search_axis = None, **kwargs):

    """ Map a set of slices according to the search dictionary.
        Search if performed in order.
        If multiple entries are found for the same key, option to concatenate.
    """

    smap = {}
    assigned = [False] * len(df_slices) # All slices are unassigned
    for key, elem in search_dict.items():
        smap[key] = []
        if ',' not in elem:
            """ Loop through unssigned slices and find string """
            for i in range(0, len(df_slices)):
                if (not assigned[i] and __map_slice(df_slices[i], elem)):
                    smap[key].append(df_slices[i])
                    assigned[i] = True

        else:
            elem_list = [x.strip() for x in elem.split(',')]

            """ Loop through unssigned slices and find list of strings """
            for i in range(0,len(df_slices)):

                check = sum([__map_slice(df_slices[i], tempStr) \
                             for tempStr in elem_list])

                if (not assigned[i] and (check == len(elem_list))):
                    smap[key].append(df_slices[i])
                    assigned[i] = True

        """ Concat dataframes is required """
        if concat_search_axis is not None and len(smap[key]) > 1:
            smap[key] = [pd.concat(smap[key], axis = concat_search_axis)]
    return smap


# In[]:
def create_df_slices(data, **kwargs):

    """ Slice data according to method specified
        full - Rows + Columns
        rows - Treat all columns as data
        columns - Treat all rows as data
    """

    method = kwargs.get("method", "full")
    data_loss = kwargs.get("data_loss", 0)

    if method in ['full', 'rows','cols']:
        df_slices = []
        slices = __get_slices(data, data_loss, method = method)

        for s in slices:
            r = s['slice']
            s_data = [[data[i][j] for j in range(r[2],r[3])] \
                       for i in range(r[0],r[1])] # Extract slice from ranges

            df = pd.DataFrame(s_data)

            """ Index and columns should reflect data types identified """
            df.index = __build_slice_index(s['index']['rows'])
            df.columns = __build_slice_index(s['index']['cols'])

            df_slices.append(df)

        return df_slices
    else: return pd.DataFrame(np.array(data))


# In[]:
def __build_slice_index(slice_index):
    index = []

    """ Index a slice based on the types - Assist in Cleaning """
    for key, value in slice_index.items():
        if value['count'] > 0:
            index.extend([str(x) + ['E','H','D'][key] \
                          for i in value['ranges']\
                          for x in range(i[0],i[1])])

    """ Sort by column and row number """
    return sorted(index, key=lambda index: int(index[:-1]))


# In[]:
def __is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def __map_value(value, file_type = None):

    """ Determine the type of a given value """
    if file_type == 'xlrd':
        return list(0, 1, 2, 2, 2, 0, 0)[value]
    else:
        if __is_number(value): return 2 # DATA
        elif type(value) is str and bool(value): return 1 # HEADING
        else: return 0 # EMPTY


# In[]:
def __get_slices(data, data_loss = 1, thresholds = {}, method = 'full'):


    """ Calculate the type density of the data provided """
    density = __calc_density(data)

    """ Default thresholds """
    if len(thresholds) == 0:
        thresholds = {"rows": __calc_threshold(density["rows"]),
                      "cols": __calc_threshold(density["cols"])}

    if data_loss < 1: # Overrides EMPTY threshold
        thresholds["rows"][0] = max(1 - data_loss, 0.6)
        thresholds["cols"][0] = max(1 - data_loss, 0.6)

    if method == "rows": # Ensures cols are treated as data
        thresholds["cols"][0] = 10
        thresholds["cols"][1] = 10

    elif method == "cols": # Ensures rows are treated as data
        thresholds["rows"][0] = 10
        thresholds["rows"][1] = 10

    """ Calculate ROW SLICES, COLUMN SLICES, then concatenate """
    rslices = __slice_data(density["rows"], thresholds["rows"])
    cslices = __slice_data(density["cols"], thresholds["cols"])
    slices = __concat_slices(rslices, cslices, data)

    """ Sort them by size - Assumption is largest slice is data """
    return sorted(slices, key=lambda slices: slices["shape"]["size"],
                  reverse = True)


# In[]:
def __calc_threshold(density):

    """ Find the thresholds required to assess if a record is
    a header, data or empty """
    ratios = {0:[], 1:[],  2:[]}
    threshold = {0: 0.6, 1: 0.5, 2: 0.3} # Minimum threshold

    """
    Iterate through every row's density only passing through exising types
    Calculate cells ratios from total and add it if it exceeds minimum
    """
    for row in density:
        for i in row.keys():
            ratio = row[i]/sum(row.values())
            if ratio > threshold[i]: ratios[i].append(ratio)

    """ Perform Quick statistics to identify dispersion
        A minimum of two observations is required to replace minimum  """
    for key, x in ratios.items():
        if len(x) > 1:
            threshold[key] = statistics.mean(x)
            threshold[key]-= 0.2 * statistics.stdev(x)

        """ Ensure the threshold is smaller than the first one, otherwise
            it will not capture the type given conditions are elif """
        if key > 0: threshold[key] = min(threshold[key], threshold[key - 1])

    return threshold


# In[]:
def __calc_density(data):

    """ Determine the types and counts of rows and column within a
        list of lists """

    rdensity = [[__map_value(x) for x in row] for row in data]
    cdensity = clean.clean_data(rdensity, transpose_data = True)

    """ Type of all cells within data """
    fdensity = [__map_value(x) for row in data for x in row]

    return {"rows": [dict(Counter(x)) for x in rdensity],
            "cols": [dict(Counter(x)) for x in cdensity],
            "full": dict(Counter(fdensity))}


# In[]:
def __slice_data (density, thresholds):


    """ Slice a list of list based on the content of its records using
        thredhold parameters to assign record types
    """

    START, SLICE = -1, 3 # Control Data Types
    ERROR, HEADING, DATA = 0, 1, 2 # Basic Data Types

    """
        Decisions Matrix to create slices (prev_type, cur_type) as key
        1. start_head (SH) - Begin couting records for a new HEADING section
        2. end_head (EH) - Finish counting records for current HEADING section
        3. start_data (SD) - Begin couting records for a new DATA section
        4. end_data (ED) - Finish counting records for current DATA section
        5. start_slice (SS) - Begin couting records for a new SLICE
        6. end_slice (ES) - Finish counting records for current SLICE
    """
    SH, EH, SD, ED, SS, ES = 0, 1, 2, 3, 4, 5

    DECISIONS = {(-1,0): [0,0,0,0,0,0],
                 (-1,1): [1,0,0,0,1,0],
                 (-1,2): [0,0,1,0,1,0],
                 (0,0) : [0,0,0,0,0,0],
                 (0,1) : [1,0,0,0,1,0],
                 (0,2) : [0,0,1,0,1,0],
                 (1,0) : [0,1,0,0,0,1],
                 (1,1) : [0,0,0,0,0,0],
                 (1,2) : [0,1,1,0,0,0],
                 (2,0) : [0,0,0,1,0,1],
                 (2,1) : [1,0,0,1,1,1],
                 (2,2) : [0,0,0,0,0,0]}

    slices = []

    """ index - type of rows
        items - sum of cell types in the slice """
    default_stypes = {'index':{t:{'count' :0,
                                  'ranges':[]} for t in range(ERROR, DATA +1)},
                      'items':{t:{'count':0} for t in range(ERROR, DATA + 1)}}

    """ ranges for each section"""
    default_ranges = {t:{'start':0,'end':0} for t in range(HEADING, SLICE + 1)}

    """ Initialize falg values and slice tracking dictionaries """
    cur_type, prev_type = START, START
    stypes = copy.deepcopy(default_stypes)
    ranges = copy.deepcopy(default_ranges)
    size = sum(list(density[0].values()))

    for index, x in enumerate(density):

        """ Determine type of each row according to thredhold
            If thresholds are met, then Data Type is found
            If HEADING and ERROR thredholds are 10, treat as DATA (ignore)
            If there are no ERRORS, then majority rules
            If there is no DATA and ERROR did not meet threshold, then HEADING
        """
        n = [int(x.get(i) or 0) for i in range(ERROR,SLICE)]

        if n[ERROR] >= size * thresholds[ERROR]: cur_type = ERROR
        elif n[HEADING] >= size * thresholds[HEADING]: cur_type = HEADING
        elif n[DATA] >= size * thresholds[DATA]: cur_type = DATA
        elif thresholds[HEADING] == thresholds[ERROR] == 10: cur_type = DATA
        elif n[ERROR] == 0: cur_type = max(x, key=x.get)
        elif n[DATA] == 0: cur_type = HEADING
        else: cur_type = DATA

        """ Get decision matrix for current case """
        decision = DECISIONS[(prev_type, cur_type)]

        # print(x, cur_type, prev_type, index, n)

        if index == len(density) - 1: # Last record

            """ Add the last record if it is a HEADING or DATA """
            if cur_type > ERROR:

                if decision[SH]: ranges[HEADING]['start'] = index
                if decision[SD]: ranges[DATA]['start'] = index

                for key, value in x.items():
                    stypes['items'][key]['count'] += value

                if prev_type == ERROR: # Ensure the slice has a start
                    ranges[SLICE]['start'] = index

                ranges[cur_type]['end'] = index + 1 # Ranges are non-inclusive

                s = np.array((ranges[cur_type]['start'],
                              ranges[cur_type]['end']))
                stypes['index'][cur_type]['ranges'].append(s)
                stypes['index'][cur_type]['count'] += 1
                s = None

                decision[ES] = 1

        """ Finish a specific Data Type Section """
        if (decision[EH] or decision[ED]):
            ranges[prev_type]['end'] = index
            s = np.array((ranges[prev_type]['start'],
                          ranges[prev_type]['end']))
            stypes['index'][prev_type]['ranges'].append(s)
            stypes['index'][prev_type]['count'] += 1

            s = None

        """ Finish a Slice """
        if decision[ES]:
            ranges[SLICE]['end'] = index

            if index == len(density) - 1 and cur_type > ERROR:
                ranges[SLICE]['end'] += 1

            s = np.array((ranges[SLICE]['start'], ranges[SLICE]['end']))
            ssize = ranges[SLICE]['end'] - ranges[SLICE]['start']
            slices.append({"slice": s,
                           "types": stypes,
                           "size": ssize})
            s = None

        """ Begin a new slice """
        if decision[SS] or decision[ES]:
            stypes = copy.deepcopy(default_stypes)
            ranges = copy.deepcopy(default_ranges)
            ranges[SLICE]['start'] = index

        """ Restart sections as required """
        if decision[SH]: ranges[HEADING]['start'] = index
        if decision[SD]: ranges[DATA]['start'] = index

        """ Add current record to current slice if not error """
        if cur_type > ERROR:
            for key, value in x.items(): # Ranges are non-inclusive
                stypes['items'][key]['count'] += value

            ranges[cur_type]['end'] = index
            ranges[SLICE]['end'] = index

        prev_type = cur_type

    return slices


# In[]:
def __concat_slices (sliceA, sliceB, data):

    """ Concat ROW and COLUMN slices - Get rectangular slices """
    slices = []
    for sA in sliceA:
        for sB in sliceB:
            """ Concatenate indices """
            r = np.concatenate((sA['slice'], sB['slice']), axis = 0)
            s_data = [[data[i][j] for j in range(r[2],r[3])]\
                       for i in range(r[0],r[1])]

            """ Recalculate new density """
            density = __calc_density(s_data)
            slices.append({'slice': r,
                           'shape': {'size': sA['size']*sB['size'],
                                     'rows': sA['size'],
                                     'cols': sB['size']},
                           'density': density,
                           'index': {'rows': sA['types']['index'],
                                     'cols': sB['types']['index']}})
    return(slices)


# In[]:
def __map_slice(df, regex):
    """ Find whether the current slice contains a given string """
    mask = np.column_stack([df[col].astype(str).str.contains(regex, na=False) \
                            for col in df])

    if len(df.loc[mask.any(axis=1)]): return True # Return if occurrene is 1
    else: return False
