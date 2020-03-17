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
.. module:: temp_loader
   :platform: Unix
   :synopsis: A class for loading standard tomography data in a variety of
    formats.

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""

import os
import h5py
import tempfile
import numpy as np

from savu.data.data_structures.data_types.data_plus_darks_and_flats \
    import NoImageKey
from savu.plugins.loaders.base_loader import BaseLoader
from savu.plugins.utils import register_plugin
from savu.data.data_structures.data_types.image_data import ImageData


@register_plugin
class ImageLoader(BaseLoader):
    """
    Load any FabIO compatible formats (e.g. tiffs)

    :param dataset_name: The name assigned to the dataset. Default: 'tomo'.
    :param angles: A python statement to be evaluated \
    (e.g np.linspace(0, 180, nAngles)) or a file. Default: None.
    :param frame_dim: Which dimension requires stitching? Default: 0.
    :param data_prefix: A file prefix for the data file. Default: None.
    :param dark_prefix: A file prefix for the dark field files, including the\
    folder path if different from the data. Default: None.
    :param flat_prefix: A file prefix for the flat field files, including the\
    folder path if different from the data. Default: None.
    """

    def __init__(self, name='ImageLoader'):
        super(ImageLoader, self).__init__(name)

    def setup(self):
        exp = self.exp
        data_obj = exp.create_data_object('in_data',
                                          self.parameters['dataset_name'])

        rot = 0
        detY = 1
        detX = 2
        data_obj.set_axis_labels('rotation_angle.degrees',
                                 'detector_y.pixel',
                                 'detector_x.pixel')

        data_obj.add_pattern('PROJECTION', core_dims=(detX, detY),
                             slice_dims=(rot,))
        data_obj.add_pattern('SINOGRAM', core_dims=(detX, rot),
                             slice_dims=(detY,))

        path = os.path.abspath(exp.meta_data.get("data_file"))
        data_obj.data = self._get_data_type(data_obj, path)

        self.set_rotation_angles(data_obj)

        # dummy file
        filename = path.split(os.sep)[-1] + '.h5'
        data_obj.backing_file = \
            h5py.File(os.path.join(tempfile.mkdtemp(), filename), 'a')

        data_obj.set_shape(data_obj.data.get_shape())
        self.set_data_reduction_params(data_obj)
        self._set_darks_and_flats(data_obj, path)

    def _set_darks_and_flats(self, dObj, path):
        if not self.parameters['flat_prefix']:
            return

        dObj.data = NoImageKey(dObj, None, 0)
        fdim = self.parameters['frame_dim']

        # read dark and flat images
        fpath, ffix = self._get_path(self.parameters['flat_prefix'], path)
        flat = ImageData(fpath, dObj, [fdim], None, ffix)

        if self.parameters['dark_prefix']:
            dpath, dfix = self._get_path(self.parameters['dark_prefix'], path)
            dark = ImageData(dpath, dObj, [fdim], None, dfix)
        else:
            shape = dObj.get_shape()
            dark = np.zeros([1] + [shape[i] for i in [1, 2]], dtype=flat.dtype)

        dObj.data._set_dark_path(dark)
        dObj.data._set_flat_path(flat)
        dObj.data._set_dark_and_flat()

    def _get_path(self, param, data):
        ppath, pfix = os.path.split(param)
        ppath = \
            os.path.join(data, ppath) if not os.path.isabs(ppath) else ppath
        return ppath, pfix

    def _get_data_type(self, obj, path):
        prefix = self.parameters['data_prefix']
        return ImageData(path, obj, [self.parameters['frame_dim']], None, prefix)

    def set_rotation_angles(self, data_obj):
        angles = self.parameters['angles']

        if angles is None:
            angles = np.linspace(0, 180, data_obj.data.get_shape()[0])
        else:
            try:
                angles = eval(angles)
            except:
                try:
                    angles = np.loadtxt(angles)
                except:
                    raise Exception('Cannot set angles in loader.')

        n_angles = len(angles)
        data_angles = data_obj.data.get_shape()[self.parameters['frame_dim']]
        if data_angles != n_angles:
            raise Exception("The number of angles %s does not match the data "
                            "dimension length %s", n_angles, data_angles)
        data_obj.meta_data.set("rotation_angle", angles)
