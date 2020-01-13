# Copyright 2014 Diamond Light Source Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. module:: yaml_utils
   :platform: Unix
   :synopsis: Utilities for yaml files

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""
import sys
import traceback
import yaml
from collections import OrderedDict
from yamllint.config import YamlLintConfig
from yamllint import linter

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    # 'Load all' is used so that multiple yaml documents may be appended with --- and read in also
    return yaml.load_all(stream, OrderedLoader)


def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    
    def represent_none(self, _):
        return self.represent_scalar('tag:yaml.org,2002:null', '')
    OrderedDumper.add_representer(type(None), represent_none)
    
    return yaml.dump(data, stream, OrderedDumper, **kwds)

def check_yaml_errors(data):
    config_file = open('/home/glb23482/git_projects/Savu/savu/plugins/loaders/utils/yaml_config.yaml')
    conf = YamlLintConfig(config_file)
    gen = linter.run(data, conf)
    errors = list(gen)
    return errors

def read_yaml(path):
    """
        Take the yaml file path and use ordered_loading to read in the yaml format as an ordered dict.
        ----------
        Parameters:
                - path: String
        ----------
        Return:
                - data_dict: Generator with ordered dictionaries for each yaml document.
        """
    text = open(path)
    errors = check_yaml_errors(text)
    try:
        with open(path, 'r') as stream:
            data_dict = ordered_load(stream, yaml.SafeLoader)
            return [data for data in data_dict]
    except (yaml.scanner.ScannerError, yaml.parser.ParserError) as se:
        print('Error with the yaml file %s' % path)
        for e in errors:
            print(e)
        raise
    except yaml.YAMLError as ye:
        print('Error reading the yaml structure with YamlLoader.')
        print(sys.exc_info())
        raise


def read_yaml_from_doc(docstring):
    """
    Take the docstring and use ordered_loading to read in the yaml format as an ordered dict.
    ----------
    Parameters:
            - docstring: String of information.
    ----------
    Return:
            - data_dict: Generator with ordered dictionaries for each yaml document.
    """
    errors = check_yaml_errors(docstring)
    try:
        # SafeLoader loads a subset of the YAML language, safely. This is recommended for loading untrusted input
        data_dict = ordered_load(docstring, yaml.SafeLoader)
        return data_dict
    except (yaml.scanner.ScannerError, yaml.parser.ParserError) as se:
        for e in errors:
            print(e)
        raise
    except yaml.YAMLError as ye:
        print('Error reading the yaml structure with YamlLoader.')
        print(sys.exc_info())
        raise

def dump_yaml(template, stream):
    ordered_dump(template, stream=stream, Dumper=yaml.SafeDumper,
                 default_flow_style=False)

