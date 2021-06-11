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
.. module:: base_median_filter
   :platform: Unix
   :synopsis: A base class for CPU/GPU median filter

.. moduleauthor::Daniil Kazantsev <scientificsoftware@diamond.ac.uk>

"""

import numpy as np
from savu.plugins.plugin import Plugin

class BaseMedianFilter(Plugin):

    def __init__(self, name='BaseMedianFilter'):
        super(BaseMedianFilter, self).__init__(name)

    def setup(self):
        in_dataset, out_dataset = self.get_datasets()
        out_dataset[0].create_dataset(in_dataset[0])
        in_pData, out_pData = self.get_plugin_datasets()
        in_pData[0].plugin_data_setup(self.parameters['pattern'], 'single')
        out_pData[0].plugin_data_setup(self.parameters['pattern'], 'single')

    def set_filter_padding(self, in_data, out_data):
        if (self.parameters['dimension'] == '3D'):
            padding = (self.parameters['kernel_size']-1)/2
        else:
            padding = 0
        in_data[0].padding = {'pad_multi_frames': padding}
        out_data[0].padding = {'pad_multi_frames': padding}

    def nInput_datasets(self):
        return 1

    def nOutput_datasets(self):
        return 1