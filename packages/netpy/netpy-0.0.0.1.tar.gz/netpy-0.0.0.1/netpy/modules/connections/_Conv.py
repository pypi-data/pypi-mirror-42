from netpy.modules.connections.connection import Connection
import numpy as np

class _Conv(Connection):
    """
        Abstract class for Convulutional Layers
    """

    def __init__(self, input_layer, output_layer, **kwargs):
        super().__init__(input_layer, output_layer)

        allowes_kwargs = {
                    "kernel",
        }
