from netpy.modules.layers.layer import Layer
from netpy.tools.functions import tanh, tanh_der
import numpy as np

class TanhLayer(Layer):

    """ Layer class with Tanh activation.
        f(x) = (exp(x)-(exp(-x))/(exp(x)+(exp(-x))
    """

    def __init__(self, input_dim):
        super().__init__(input_dim)
        self.error_vector = np.zeros([input_dim])
        self.der_func = tanh_der
        self.activation = 'tanh'
        self.num_of_neurons = input_dim

    def forward(self):
        self.output_vector = tanh(self.input_vector)
