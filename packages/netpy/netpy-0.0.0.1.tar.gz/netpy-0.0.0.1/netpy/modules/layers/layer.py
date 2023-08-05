from netpy.modules.module import Module
import numpy as np

class Layer(Module):

    """ Parent class for all Layers  """

    def __init__(self, input_dim):
        super().__init__(input_dim)

        self.der_func = None
        self.error_vector = np.zeros([])
        self.delta = np.zeros([input_dim])

    def __repr__(self):
        return "<dim: %s, type: %s>" % (self.input_dim, self.type)
