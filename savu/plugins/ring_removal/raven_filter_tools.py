from savu.plugins.plugin_tools import PluginTools

class RavenFilterTools(PluginTools):
    """Ring artefact removal method
    """
    def define_parameters(self):
        """
        uvalue:
            visibility: basic
            dtype: int
            description: "To define the shape of filter, e.g. bad=10,
              moderate=20, minor=50."
            default: 20
        vvalue:
            visibility: intermediate
            dtype: int
            description: How many rows to be applied the filter.
            default: 2
        nvalue:
            visibility: intermediate
            dtype: int
            description: To define the shape of filter
            default: 4
        padFT:
            visibility: intermediate
            dtype: int
            description: Padding for Fourier transform.
            default: 20
        """

    def get_citation(self):
        """
        citation1:
            description: The ring artefact removal algorithm used in this
              processing chain is taken from this work.
            bibtex: |
                    @article{raven1998numerical,
                    title={Numerical removal of ring artifacts in microtomography},
                    author={Raven, Carsten},
                    journal={Review of scientific instruments},
                    volume={69},
                    number={8},
                    pages={2978--2980},
                    year={1998},
                    publisher={American Institute of Physics}
                    }
            endnote: |
                    %0 Journal Article
                    %T Numerical removal of ring artifacts in microtomography
                    %A Raven, Carsten
                    %J Review of scientific instruments
                    %V 69
                    %N 8
                    %P 2978-2980
                    %@ 0034-6748
                    %D 1998
                    %I American Institute of Physics
            doi: "10.1063/1.1149043"
        """