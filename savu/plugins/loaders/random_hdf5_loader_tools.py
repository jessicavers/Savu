from savu.plugins.plugin_tools import PluginTools

class RandomHdf5LoaderTools(PluginTools):
    """A hdf5 dataset of a specified size is created at runtime using numpy
random sampling (numpy.random) and saved to file. This created dataset
will be used as the input file, and the input file path passed to Savu
will be ignored (use a dummy).
    """
    def define_parameters(self):
        """
        size:
              visibility: basic
              dtype: list
              description: A list specifiying the required data size.
              default: []
        axis_labels:
              visibility: basic
              dtype: list
              description: "A list of the axis labels to be associated
                with each dimension, of the form ['name1.unit1', 'name2.unit2',...]"
              default: []
        patterns:
              visibility: intermediate
              dtype: list
              description: "A list of data access patterns e.g.
                [SINOGRAM.0c.1s.2c, PROJECTION.0s.1c.2s], where
                'c' and 's' represent core and slice dimensions
                respectively and every dimension must be
                specified."
              default: []
        file_name:
              visibility: intermediate
              dtype: filename
              description: Assign a name to the created h5 file.
              default: input_array
        dtype:
              visibility: intermediate
              dtype: nptype
              description: A numpy array data type
              default: 'int16'
        dataset_name:
              visibility: intermediate
              dtype: str
              description: The name assigned to the dataset
              default: 'tomo'
        angles:
              visibility: intermediate
              dtype: str
              description: "A python statement to be evaluated or a
                file - if the value is None, values will be in the
                interval [0, 180]"
              default: None
        pattern:
              visibility: intermediate
              dtype: str
              description: Pattern used to create and store the hdf5 dataset
                default is the first pattern in the pattern dictionary.
              default: None
        range:
              visibility: intermediate
              dtype: range
              description: Set the distribution interval.
              default: [1, 10]

        """