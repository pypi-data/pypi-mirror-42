from netpy.modules.module import Module
import numpy as np

class Connection(Module):

    """
        Parent class for all connections.
        Constructor gets two layers.
    """

    def __init__(self, input_layer, output_layer):

        self.input_dim = input_layer.input_dim
        self.output_dim = output_layer.input_dim

        self.input_layer = input_layer
        self.output_layer = output_layer

        self.weight_delta = np.zeros([])
        self.weight_delta_old = np.zeros((self.input_dim, self.output_dim))

        super().__init__(self.input_dim, self.output_dim)
