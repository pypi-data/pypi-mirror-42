from netpy.modules.layers.layer import Layer
from netpy.tools.functions import SoftPlus, SoftPlus_der
import numpy as np

class SoftPlusLayer(Layer):

    """ Layer class with SoftPlus activation.
        f(x) = log(1+exp(x))
    """

    def __init__(self, input_dim):
        super().__init__(input_dim)
        self.error_vector = np.zeros(input_dim)
        self.der_func = SoftPlus_der
        self.activation = 'softplus'
        self.num_of_neurons = input_dim

    def forward(self):
        self.output_vector = SoftPlus(self.input_vector)
