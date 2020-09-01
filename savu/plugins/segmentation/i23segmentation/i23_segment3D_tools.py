from savu.plugins.plugin_tools import PluginTools

class I23Segment3dTools(PluginTools):
    """A Plugin to segment reconstructed data from i23 beamline. The projection data
should be first reconstructed iteratively using the ToMoBAR plugin. The goal of
the segmentation plugin is to cluster and segment data using Gaussian Mixtures
and then apply iterative model-based segmentation to further process the obtained mask
INPUT to the plugin is the result of gmm_segment plugin
    """
    def define_parameters(self):
        """
        classes:
            visibility: intermediate
            dtype: int
            description: The number of classes for GMM.
            default: 5

        correction_window:
            visibility: basic
            dtype: int
            description: The size of the correction (non-local) window
            default: 8

        iterations:
            visibility: basic
            dtype: int
            description: The number of iterations for segmentation.
            default: 10

        """