#!/usr/bin/env python
# coding: utf-8

# Developer: Carlos Hernandez (cseHdz)
# Date: October 2018
from dextract.models.layers import BaseLayer

# Standard packages
import pandas as pd
from collections import Counter

# In[]:
class Sequential:

    def __init__(self):
        self.layers = {}
        self.layer_count = 0
        self.output = None


    def add_at_index(self, index, layer):

        self.add(layer)
        if index < self.layer_count - 1:
            names = self.get_layer_names()
            last_layer_key = names[-1]
            """ Add all layers from beg. to before the index """
            beg = {key: self.layers[key] for i, key in enumerate(names) \
                   if i < index}

            beg[last_layer_key] = self.layers[last_layer_key]
            end = {key: self.layers[key] for i, key in enumerate(names) \
                   if i >= index and key != last_layer_key}

            self.layers = {**beg, **end}

    def add(self, layer):

        if not issubclass(type(layer), BaseLayer):
            print('Invalid Data Type')
            return None

        layer_type = type(layer).__name__
        if layer_type not in ['Cleaner', 'Slicer', 'Extractor', 'Flattener']:
            return "Can't add layer - Unknown type"

        type_count = [int(key[-1]) for key, item in self.layers.items()\
                      if item['layer_type'] == layer_type]


        type_index = max(type_count) + 1 if len(type_count) > 0 else 0

        layer_name = layer_type + '_' + str(type_index)

        self.layers[layer_name] = {'layer_type': layer_type,
                                   'layer_params': layer.parameters,
                                   'layer': layer}

        self.layer_count = self.layer_count + 1

    def delete(self, layer_name):
        if layer_name in self.layers.keys():
            del self.layers[layer_name]
            self.layer_count = self.layer_count - 1


    def get_layer(self, layer_name):
         if layer_name in self.layers.keys(): return self.layers[layer_name]
         else: return None

    def get_layer_names(self):
        return list(self.layers.keys())

    def summary(self):

        types = []
        params = []
        names = list(self.layers.keys())
        for layer in self.layers.values():
            types.append(layer['layer_type'])
            params.append(layer['layer_params'])

        summ = {'Name': names, 'Type': types, 'Parameters': params}
        layers_summary = pd.DataFrame.from_dict(summ)
        layer_count = len(names)
        layer_types = dict(Counter(types))

        print('Layer Count: ', layer_count)
        print('Layer Types: ', layer_types)
        print('--------- Model Details ---------')
        print(layers_summary)

        return {'layers_summary': layers_summary,
                'layers_count': layer_count,
                'layer_types': layer_types}

    def __run_layer(self, layer, layer_name, data):

        result = None
        if data is None and layer.data_input is not None:
            data = layer.data_input

        if data is None and layer.data_required:
            return 'Data Input required for layer ' + layer_name
        elif not layer.data_required: result = layer.run()

        elif layer.run_type == 'multiple' or layer.run_type == 'dict':
            if not isinstance(data, dict):
                print (layer_name, ' - Keys were not found in previous layer')
                return None
            result = layer.run(data)
        else:
            if isinstance(data, pd.DataFrame):
                result = layer.run(data)
                return result

            elif isinstance (data, list):

                if all([isinstance(k, pd.DataFrame) for k in data] or\
                        [isinstance(k, dict) for k in data]):
                    result =[]
                    for d in data:
                        temp = self.__run_layer(layer, layer_name, d)

                        """ Extend a list, or append Dataframe """
                        if isinstance(temp, list): result.extend(temp)
                        else: result.append(temp)
                else: result = layer.run(data)
                return result

            elif isinstance(data, dict):

                result = {}
                for key, item in data.items():
                    temp = self.__run_layer(layer, layer_name, item)
                    result[key] = temp
                return result

        return result

    def __run_level(self, level, data):
        output = {}

        curr_layer_name = self.get_layer_names()[level]
        curr_layer = self.layers[curr_layer_name]['layer']

        if curr_layer.mode == 'forward':
           output = self.__run_layer(curr_layer, curr_layer_name, data)

           if output is None: return None
           """ Pass forward if there is a subsequent level """
           if level < self.layer_count - 1:
               output = self.__run_level(level + 1, data = output)

        elif curr_layer.mode == 'backward':
            data = self.__run_level(level + 1, data = data)
            output = self.__run_layer(curr_layer, curr_layer_name, data)

        return output


    def run(self, data = None, level = 0):

        self.output = self.__run_level(level, data)
        return self.output
