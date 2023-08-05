from netpy.tools.functions import *
from netpy.teachers.teacher import Teacher
import numpy as np
import math

class BackPropTeacherTest(Teacher):

    """ Class for teaching net with Back Prop """

    def __init__(self, net, **kwargs):
        super().__init__(net, **kwargs)

        self.out_weights_delta = np.zeros([])
        self.net = net
        self.output_vector = net.modules[-1].output_vector

        self.net.teacher = "BackPropTeacher"

    def train(self, test, ideal, num_of_epoch, **kwargs):
        super().train(test, ideal, num_of_epoch, **kwargs)

    def __forward_err(self, test, ideal, output):

        for k in range(1, len(self.net.modules)-1, 2):

            output = self.net.modules[k-1].output_vector
            input_dim = self.net.modules[k].input_dim
            output_dim = self.net.modules[k].output_dim

            self.net.modules[k].weight_delta = np.zeros((input_dim, output_dim))

            for n in range(len(output)):
                for m in range(len(self.net.modules[k+1].delta)):

                    self.net.modules[k].weight_delta[n, m] = (np.dot(output[n],
                                                              self.net.modules[k+1].delta[m])*
                                                              self.learning_rate[0])

            norm_old = NormMatrix(self.net.modules[k].weight_delta_old)


            if norm_old < 1:
                norm_old = 1

            scal_w = ScalarMultMatrix(self.net.modules[k].weight_delta_old,
                                      self.net.modules[k].weight_delta)/norm_old


            for n in range(len(output)):
                for m in range(len(self.net.modules[k+1].delta)):

                    self.net.modules[k].weight_delta[n, m] -= (self.net.modules[k].weight_delta_old[n,m]*
							       scal_w)

            for n in range(len(output)):
               for m in range(len(self.net.modules[k+1].delta)):
                    self.net.modules[k].weight_matrix[n, m] -= (self.net.modules[k].weight_delta[n, m] -
                                                                self.net.modules[k].weight_delta_old[n, m]*
                                                                self.learning_rate[1])

                    self.net.modules[k].weight_delta_old[n, m] += self.net.modules[k].weight_delta[n, m]

            norm_old = NormMatrix(self.net.modules[k].weight_delta_old)

            if norm_old > 1:
                self.net.modules[k].weight_delta_old /= norm_old


    def backward(self, test, ideal, output):
        error = output - ideal

        self.net.modules[-1].delta = (error*
                                      self.net.modules[-1].der_func(output))

        for i in range(len(self.net.modules)-3, 0, -2):

            delta = self.net.modules[i+2].delta

            self.net.modules[i].error_vector = delta.dot(
                                         self.net.modules[i+1].weight_matrix.T)

            for err in range(len(self.net.modules[i].error_vector)):
                for ders in range(len(output)):

                    self.net.modules[i].delta[err] = (self.net.modules[i].error_vector[err]*
                                                      self.net.modules[i].der_func(output[ders]))

        self.__forward_err(test, ideal, output)
        loss = mse_Error(output, ideal)

        return loss
