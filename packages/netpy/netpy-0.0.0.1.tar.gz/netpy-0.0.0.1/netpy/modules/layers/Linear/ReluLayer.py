from netpy.modules.layers.layer import Layer
from netpy.tools.functions import ReLU, ReLU_der
import numpy as np

class ReluLayer(Layer):

    """ Layer class with ReLU activation.
        if x < 0:
            return 0
        return x
    """

    def __init__(self, input_dim):
        super().__init__(input_dim)
        self.error_vector = np.zeros(input_dim)
        self.der_func = ReLU_der
        self.activation = 'relu'
        self.num_of_neurons = input_dim

    def forward(self):
        self.output_vector = ReLU(self.input_vector)
