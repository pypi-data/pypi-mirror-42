from netpy.modules.layers.layer import Layer
from netpy.tools.functions import SoftSign, SoftSign_der
import numpy as np

class SoftSignLayer(Layer):

    """ Layer class with SoftSign activation.
        f(x) = x/(1+abs(x))
    """

    def __init__(self, input_dim):
        super().__init__(input_dim)
        self.error_vector = np.zeros(input_dim)
        self.der_func = SoftSign_der
        self.activation = 'softsign'
        self.num_of_neurons = input_dim

    def forward(self):
        self.output_vector = SoftSign(self.input_vector)
