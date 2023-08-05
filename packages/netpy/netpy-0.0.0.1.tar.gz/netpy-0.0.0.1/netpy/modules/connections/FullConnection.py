from netpy.modules.connections.connection import Connection
import numpy as np

class FullConnection(Connection):

    """
        Each neuron is connected to each one.
    """

    def __init__(self, input_layer, output_layer):
        super().__init__(input_layer, output_layer)

        """ Init weights with random numbers """
        self.weight_matrix = np.random.randn(self.input_dim, self.output_dim)
        self.weight_delta = None
        self.weight_delta_sum = 0
        self.delta_weight_old = np.zeros((self.input_dim, self.output_dim))

        self.type = 'full'
        self.input_dim = self.input_dim
        self.output_dim = self.output_dim

    def __repr__(self):
        return "<FullConnection>"

    def forward(self):
        """ Function for activation of neurons  """
        self.output_vector = np.dot(self.input_layer.output_vector, self.weight_matrix)
        self.output_layer.input_vector = self.output_vector
