import numpy as np

class Module:

    """
        Parent class for layers and relations
        Constructor get vars of input and output signals
    """

    def __init__(self, input_dim, output_dim = None):

        self.input_dim = input_dim

        if output_dim is not None:
            self.output_dim = output_dim
        
        # Init input and output vectors with zeros
        self.input_vector = np.zeros(input_dim)
        self.output_vector = np.zeros(output_dim)
