from savu.plugins.plugin_tools import PluginTools

class CcpiCglsReconTools(PluginTools):
    """A Plugin to run the CCPi implementation of the CGLS reconstruction
algorithm.
    """

    def define_parameters(self):
        """

        n_iterations:
            visibility: basic
            dtype: tuple
            description: Number of rows and columns in the reconstruction.
            default: 5

        resolution:
            visibility: basic
            dtype: str
            description: Number of output voxels (res = n_pixels/n_voxels),
              set res > 1 for reduced resolution.
            default: 1

        n_frames:
            visibility: basic
            dtype: int
            description:  This algorithm requires a multiple of 8 frames for
              processing and this number may affect performance depending on
              your data size (choose from 8, 16, 24, 32)
            options: [8,16,24,32]
            default: 16

        outer_pad:
            visibility: advanced
            dtype: str
            description: Not an option.
            default: False

        centre_pad:
            visibility: hidden
            dtype: int
            description: Not an option.
            default: False

        init_vol:
            visibility: advanced
            dtype: str
            description: Not an option.
            default: None

        enforce_position:
            visibility: advanced
            dtype: int
            description: Not an option.
            default: False

        """
