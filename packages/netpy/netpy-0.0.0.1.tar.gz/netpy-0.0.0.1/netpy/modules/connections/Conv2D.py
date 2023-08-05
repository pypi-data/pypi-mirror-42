from netpy.modules.connections._Conv import _Conv
import numpy as np

class Conv2D(_Conv):
    def __init__(self, input_layer, output_layer, kernel):
        super().__init__(input_layer, output_layer, kernel)

        
        # NUMPY.CONVOLVE
