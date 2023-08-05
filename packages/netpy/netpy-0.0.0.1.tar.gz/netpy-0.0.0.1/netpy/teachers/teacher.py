from netpy.tools.errors import *
import json
import random
import logging
import datetime
import numpy as np
import os
import signal
import sys
import h5py


class Teacher:

    """ Parent class for teachers  """

    def __init__(self, net, **kwargs):

        allowed_kwargs = {
                "error",        # TODO
        }

        errors = {
                "MSE": mse_Error    # TODO
        }

        self.net = net
        self.learning_rate = kwargs.get('learning_rate')

        self.net.learning_rate = self.learning_rate
        self.net.error = kwargs.get('error')

        self.save_state = False

    def __signal_handler(self, sig, frame):
        
        print('\nStop training...')

        if self.save_state == True:
            print('Everything is OK...')
        else:
            print('Saving data...')
            json_data = {
                              'net':{
                                'name': self.net.name,
                                'total_epoch': self.net.total_epoch,
                                'parent': None,
                                'loss': None,

                                'arch':{
                                    'layers':[],
                                    'connections':[]
                                },

                                'iq_test': {
                                    'iq': None,
                                    'iq_min': None,
                                    'iq_max': None,
                                    'num_of_tests': None
                                    }
                               },

                               'train_parameters': {
                                    'teacher': None,
                                    'learning_rate': None,
                                    'error': None
                                },
                                'description': ''
                            }
            
            print('Saving json-file...')
            with open(self.net.path_data+self.net.name+'.json', 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            
            os.remove(self.net.path_data+self.net.name+'.h5')

            data = h5py.File(self.net.path_data+self.net.name+'.h5', 'w')

            print('Saving h5-file...')
            for i in range(1, len(self.net.modules), 2):
                data.create_dataset('weights_'+str(i-1)+'_'+str(i+1),
                                data=self.net.modules[i].weight_matrix,
                                maxshape=(None, None))

            data.close()
            self.net.save()

        print('Done')
        sys.exit(0)

    def __forward_train(self, test, ideal, name_of_answer, save_output_data):

        signal.signal(signal.SIGINT, self.__signal_handler)
        logging.basicConfig(filename=self.net.path_data+self.net.name+'.log',
                            level=logging.INFO)

        self.save_state = False
        output = self.net.forward(test, True)
        Loss = self.backward(test, ideal, output)
        self.net.total_epoch += 1
        self.net.loss = Loss
        self.net.save()
        self.save_state = True

        output_new = self.net.forward(test, True)

        LossNew = mse_Error(output_new, ideal)

        if self.logging is not False:

            logging.info("%s | Training | Epoch: %s | Name Of Answer: %s | Loss: %s | Loss New: %s" %
                (datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"),
                    self.net.total_epoch, name_of_answer, Loss, LossNew))


        print("%s | Training | Epoch: %s | Name Of Answer: %s | Loss: %.4f | Loss New: %.4f" %
                (datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"),
                    self.net.total_epoch, name_of_answer, Loss, LossNew))

        if save_output_data == True:

            if not os.path.isdir(self.net.name+'_data/outputs'):
                os.makedirs(self.net.name+'_data/outputs')

            np.savetxt(self.net.name+'_data/outputs/output.txt', output)
            np.savetxt(self.net.name+'_data/outputs/test.txt', test)

        

    def train(self, test, ideal, num_of_epoch, **kwargs):

        allowed_kwargs = {
                    'name_of_answer',
                    'random_data',
                    'save_output_data',
                    'learning_rate',
                    'logging'
        }

        for kwarg in kwargs:
            if kwarg not in allowed_kwargs:
                raise TypeError("I don't know what are you want from me")


        name_of_answer = kwargs.get('name_of_answer')
        self.logging = kwargs.get('logging')

        if name_of_answer is None:
            name_of_answer = ideal

        random_data = kwargs.get('random_data')
        save_output_data = kwargs.get('save_output_data')

        self.learning_rate = kwargs.get('learning_rate')

        if self.net.load_weights_bool is False:
            self.net.total_epoch = 0

        if random_data == False:

            if num_of_epoch // len(test) > 0:
                for i in range(num_of_epoch // len(test)):
                    for j in range(len(test)):
                        self.__forward_train(test[j], ideal[j], name_of_answer[j], save_output_data)

                if num_of_epoch % len(test) > 0:
                    for j in range(num_of_epoch % len(test)):
                        self.__forward_train(test[j], ideal[j], name_of_answer[j], save_output_data)

            else:
                for j in range(num_of_epoch):
                    self.__forward_train(test[j], ideal[j], name_of_answer[j], save_output_data)


        else:
            for i in range(num_of_epoch):
                j = int(random.uniform(0, len(ideal)))
                self.__forward_train(test[j], ideal[j], name_of_answer[j], save_output_data)

    def backward(self, test, ideal, output):
        pass
