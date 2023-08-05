import h5py
import numpy
import json
import os
import time
import logging
import datetime
from netpy.modules import *

class Net:

    """ Parent class Net """

    def __init__(self, name):

        # Struct of net, must be input_layer->relation->hidden_layer->...->output_layer
        self.modules = []

        self.name = name

        if not os.path.isfile('conf.json'):
            conf_data = {
                            "name": name,
                            "data_dir": ''
                        }

            with open('conf.json', 'w') as log:
                log.write(json.dumps(conf_data, indent=4))

        self.total_epoch = 0
        self.loss = 0

        self.iq = 0
        self.iq_min = 0
        self.iq_max = 0
        self.num_of_tests = 0

        self.teacher = 0
        self.learning_rate = 0
        self.error = 0

        self.description = 0

        self.load_weights_bool = False

        with open('conf.json', 'r') as log:
            json_data = json.load(log)
            self.path_data = json_data['data_dir']

    def __str__(self):
        return "%s" % self.modules[:]

    def add_Input_Layer(self, layer):

        """ Function for add input layer  """

        try:

            self.modules[0].type = "Hidden"
            new_modules = [layer]
            new_modules.extend(self.modules)
            self.modules = new_modules

        except IndexError:
            self.modules.append(layer)

        self.modules[0].type = "In"

    def add_Layer(self, layer):

        """ Function for add layer  """

        if self.modules[-1].type == "Out":
            self.modules.append(0)
            self.modules[-1], self.modules[-2] = self.modules[-2], layer
            self.modules[-2].type = "Hidden"
        else:
            self.modules.append(layer)
            self.modules[-1].type = "Hidden"

    def add_Output_Layer(self, layer):

        """ Function for add output layer  """

        if self.modules[-1].type == "Out":
            self.modules[-1].type = "Hidden"

        self.modules.append(layer)
        self.modules[-1].type = "Out"

    def add_Connection(self, connection):

        """ Function for add Connection module  """

        first_index = self.modules.index(connection.input_layer)
        second_index = self.modules.index(connection.output_layer)

        tmp_modules = self.modules[second_index:]

        del self.modules[second_index:]

        self.modules.append(connection)
        self.modules.extend(tmp_modules)

    def forward(self, array, training=False):

        """ Function for activate a Net  """

        self.modules[0].input_vector = array

        for module in self.modules:
            module.forward()

        if training == False:

            time = datetime.datetime.today().today().strftime("%Y-%m-%d-%H.%M.%S")
            logging.basicConfig(filename=self.path_data+self.name+'.log',
                                level=logging.INFO)

            logging.info("%s | test | input: %s | output: %s | Loss: %s" %
                        (time, self.modules[0].input_vector, self.modules[-1].output_vector, 0))

        return self.modules[-1].output_vector

    def save(self, path = None, name_W = None):

        """ Function for save a Net  """

        if path is None:
            with open('conf.json', 'r') as outfile:
                json_data = json.load(outfile)
                self.path_data = json_data['data_dir']

        else:
            self.path_data = path

        if name_W is None:
            name_W = self.name

        if not os.path.isfile(self.path_data+'arch.json'):

            json_data = {
                              'net':{
                                'name': self.name,
                                'total_epoch': None,
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

            with open(self.path_data+'arch.json', 'w') as outfile:
                json.dump(json_data, outfile, indent=4)

        layers_arr = []
        connections_arr = []

        with open(self.path_data+'arch.json', 'r') as outfile:
            json_data = json.load(outfile)
            json_data['net']['name'] = self.name
            json_data['net']['total_epoch'] = self.total_epoch
            json_data['net']['iq_test']['iq'] = self.iq
            json_data['net']['iq_test']['iq_min'] = self.iq_min
            json_data['net']['iq_test']['iq_max'] = self.iq_max
            json_data['net']['iq_test']['num_of_tests'] = self.num_of_tests

            if json_data['net']['loss'] is None:
                loss_old = 0
            else:
                loss_old = json_data['net']['loss']

            json_data['net']['loss'] = 0.1*self.loss + 0.9*loss_old

            json_data['train_parameters']['teacher'] = self.teacher
            json_data['train_parameters']['learning_rate'] = self.learning_rate
            json_data['train_parameters']['error'] = self.error

            for i in range(0, len(self.modules), 2):
                layers_arr.append({'num_of_neurons':self.modules[i].num_of_neurons,
                                   'activation':self.modules[i].activation})

            for i in range(1, len(self.modules), 2):
                connections_arr.append({'type':self.modules[i].type,
                                        'input_dim':self.modules[i].input_dim,
                                        'output_dim':self.modules[i].output_dim})


            json_data['net']['arch']['layers'] = layers_arr
            json_data['net']['arch']['connections'] = connections_arr


        with open(self.path_data+'arch.json', 'w') as outfile:
            outfile.write(json.dumps(json_data, indent=4))

        self.save_weights(self.path_data + 'weights.h5')

    def save_weights(self, filename):
        data = h5py.File(filename, 'w')

        for i in range(1, len(self.modules), 2):
            data.create_dataset('weights_'+str(i-1)+'_'+str(i+1),
                                data=self.modules[i].weight_matrix,
                                maxshape=(None, None))

        data.close()


    def load_net_data(self, path = None, name_W = None):

        """ Function for load a Net  """

        layers = {
                "linear": LinearLayer,
                "relu": ReluLayer,
                "sigmoid": SigmoidLayer,
                "softplus": SoftPlusLayer,
                "softsign": SoftSignLayer,
                "tanh": TanhLayer
        }

        connections = {
                "full": FullConnection
        }

        if path is None:

            with open('conf.json', 'r') as log:
                data = json.load(log)
                self.path_data = data['data_dir']

        else:

            self.path_data = path

        if name_W is None:
            name_W = self.name

        with open(self.path_data+'arch.json', 'r') as log:
            data = json.load(log)
            self.name = data['net']['name']
            self.total_epoch = data['net']['total_epoch']

            self.iq = data['net']['iq_test']['iq']
            self.iq_min = data['net']['iq_test']['iq_min']
            self.iq_max = data['net']['iq_test']['iq_max']
            self.num_of_tests = data['net']['iq_test']['num_of_tests']

            for i in range(len(data['net']['arch']['layers'])):
                activation = data['net']['arch']['layers'][i]['activation']
                input_dim = data['net']['arch']['layers'][i]['num_of_neurons']
                if i == 0:
                    self.add_Input_Layer(layers[activation](input_dim))
                elif i == len(data['net']['arch']['layers']) - 1:
                    self.add_Output_Layer(layers[activation](input_dim))
                else:
                    self.add_Layer(layers[activation](input_dim))

            connection_arr = []

            for i in range(len(data['net']['arch']['connections'])):
                connection_type = data['net']['arch']['connections'][i]['type']
                connection_arr.append(connections[connection_type](self.modules[i], self.modules[i+1]))

            for i in range(len(connection_arr)):
                self.add_Connection(connection_arr[i])

    def load_weights(self, path = None, name_W = None):

        self.load_weights_bool = True

        if path is None:
            with open('conf.json', 'r') as log:
                data = json.load(log)
                self.path_data = data['data_dir']
        else:
            self.path_data = path

        if name_W is None:
            name_W = self.name

        data = h5py.File(self.path_data + 'weights.h5', 'r')

        for i in range(1, len(self.modules), 2):

            current_matrix = data['weights_'+str(i-1)+'_'+str(i+1)][:]

            for m in range(len(current_matrix)):
                for n in range(len(current_matrix[0])):
                    self.modules[i].weight_matrix[m][n] = current_matrix[m][n]

        data.close()
