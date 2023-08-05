#!/usr/bin/env python
# coding: utf-8

# Developer: Carlos Hernandez (cseHdz)
# Date: October 2018

# User defined
from dextract.helpers import slicing, clean, extract, flatten

# Standard packages
import pandas as pd
import numpy as np

# In[]:
class BaseLayer:
    def __init__(self, run_type, parameters, mode, data_required = False):

        self.mode = mode
        self.run_type = run_type
        self.parameters = parameters
        self.data_input = None
        self.data_output = None
        self.data_required = data_required

    def run(self):
        raise NotImplementedError


# In[]:
class DataLayer(BaseLayer):

    def __init__(self, run_type, parameters, mode = 'forward'):
        super().__init__(run_type, parameters, mode, data_required = True)

    def _run(self, data, **kwargs):
        raise NotImplementedError

    def _multirun(self, data_dict):
        output = {}

        for key, data in data_dict.items():

            if isinstance(data, dict): output[key] = self._multirun(data)

            elif key in self.parameters.keys():

                param = self.parameters[key]

                if isinstance(data, pd.DataFrame):
                    output[key] = self._run(data, **param)

                elif isinstance (data, list):
                    if all([isinstance(k, pd.DataFrame) for k in data]):

                        output[key] = []
                        for d in data:
                            temp = self._run(d, **param)

                            """ Extend a list, or append Dataframe """
                            if isinstance(temp, list): output[key].extend(temp)
                            else: output[key].append(temp)

                    if all([isinstance(k, list) for k in data]):
                        output[key] = self._run(data, **param)

                else:
                    print('Wrong Data Format')
                    output[key] = 'Failed to process key: ' + str(key)
            else: output[key] = data

        return output

    def run(self, data = None):

        if data is None and self.data_input is not None: data = self.data_input
        elif data is not None: self.data_input = data
        else: return None

        if isinstance(data, dict): result = self._multirun(data)
        elif isinstance(data, pd.DataFrame) or isinstance(data, list):

            result = self._run(data, **self.parameters)
        else: result = 'Invalid data format'

        self.data_output = result

        return result


# In[]:
class Slicer(DataLayer):

    def __init__(self, data_loss = 1, method = "full",
                 run_type = 'single', **kwargs):

        if method not in ['full', 'rows','cols']: print('Invalid method')
        parameters = {'data_loss': data_loss, 'method': method, **kwargs}

        if all([isinstance(k, dict) for k in kwargs.values()]):
            run_type = 'multiple'

        super().__init__(run_type, parameters)

    def _run(self, data, **kwargs):
        if isinstance(data, pd.DataFrame): data = data.values.tolist()
        result = slicing.extract_slices(data, **kwargs)
        return result


# In[]:
class Cleaner(DataLayer):

    def __init__(self, clean_type = 'df', run_type = 'single', **kwargs):

        if clean_type not in ['data', 'df']: print('Invalid data type')
        parameters = {'type': clean_type, **kwargs}

        if all([isinstance(item, dict) and 'rename_' not in key \
                and 'add_columns' not in key for key, item in kwargs.items()]):
            run_type = 'multiple'

        super().__init__(run_type, parameters)


    def __clean(self, data, key, param):

        clean_type = self.parameters['type']
        clean_dict = {key: param}

        if clean_type == 'data':
            if isinstance(data, pd.DataFrame): data = data.values.tolist()
            data = clean.clean_data(data, **clean_dict)
        elif clean_type == 'df':
            if isinstance(data, list): data = pd.DataFrame(np.array(data))
            data = clean.clean_df(data, **clean_dict)

        return data


    def _run(self, data, **kwargs):

        result = data
        for key, param in kwargs.items():
            result = self.__clean(result, key, param)
            if isinstance(result, str): break
        return result


# In[]:
class Extractor(BaseLayer):

    def __init__(self, ext_type, path, file_name, **kwargs):
        if ext_type not in ['xl', 'csv', 'sheet']: print('Invalid data type')
        parameters = {'type': ext_type, 'path': path, 'file_name': file_name,
                      **kwargs}

        super().__init__(None, parameters, 'forward')

    def run(self):
        ext_type = self.parameters['type']
        if ext_type == 'xl':
            if self.parameters.get('sheets') is None:
                return 'No sheets specified'
            self.data_output = extract.data_from_xl(**self.parameters)

        elif ext_type == 'sheet':
            if self.parameters.get('sheet_name') is None:
                return 'No sheet name specified'
            self.data_output = extract.data_from_xl_sheet(**self.parameters)

        elif ext_type == 'csv':
            self.data_output = extract.data_from_csv(**self.parameters)

        return self.data_output


# In[]:
class Flattener(BaseLayer):

    def __init__(self, df_names, dict_name, **kwargs):

        if isinstance(df_names, list): key = 'name_from_list'
        elif isinstance(df_names, dict): key = 'name_from_dictionary'

        parameters = {key: df_names, 'dict_name': dict_name, **kwargs}

        super().__init__('dict', parameters, 'forward', data_required = True)

    def run(self, data):

        if data is None and self.data_input is not None: data = self.data_input
        elif data is not None: self.data_input = data
        else: return None

        self.data_output = flatten.pop_keys_df_dict(data, **self.parameters)
        return self.data_output
