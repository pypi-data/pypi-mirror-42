from netpy.modules.layers.layer import Layer

class LinearLayer(Layer):

    """ Layer class with f(x)=x activation.  """

    def __init__(self, input_dim):
        super(Layer, self).__init__(input_dim)
        self.activation = 'linear'
        self.num_of_neurons = input_dim

    def forward(self):
        self.output_vector = self.input_vector
