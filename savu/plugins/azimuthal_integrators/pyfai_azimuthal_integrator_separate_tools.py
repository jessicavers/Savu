from savu.plugins.plugin_tools import PluginTools

class PyfaiAzimuthalIntegratorSeparateTools(PluginTools):
    """1D azimuthal integrator by pyFAI
    """
    def define_parameters(self):
        """
        use_mask:
              visibility: basic
              dtype: bool
              description: Should we mask.
              default: False
        out_datasets:
              visibility: datasets
              dtype: list
              description: A
              default: ['powder','spots']
        percentile:
              visibility: intermediate
              dtype: int
              description: Percentile to threshold
              default: 50
        num_bins:
              visibility: basic
              dtype: int
              description: Number of bins.
              default: 1005
        num_bins_azim:
              visibility: basic
              dtype: int
              description: Number of azimuthal bins.
              default: 20

        """