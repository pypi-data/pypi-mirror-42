from netpy.modules.layers.layer import Layer
from netpy.tools.functions import sigmoid, sigmoid_der
import numpy as np

class SigmoidLayer(Layer):

    """ Layer class with Sigmoid activation.
        f(x) = 1/(1+exp(-x))
    """

    def __init__(self, input_dim):
        super().__init__(input_dim)
        self.error_vector = np.zeros(input_dim)
        self.der_func = sigmoid_der
        self.activation = 'sigmoid'
        self.num_of_neurons = input_dim

    def forward(self):
        self.output_vector = sigmoid(self.input_vector)
