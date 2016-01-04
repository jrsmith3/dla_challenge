import network
import time
import json
import itertools
import numpy as np

def convert_dat(datum):
    """
    Convert dict data output by tec to tuple for neural net
    
    This function converts dictionary data output by the `tec` module
    to the 2-tuple format required by the NNADL [1] code.
    The zeroth element of the 2-tuple is a numpy array containing the
    independent variables, and the first element is the dependent variable.
    This function orders the independent variables from the dict to the 
    numpy array as follows:
    
    * collector barrier
    * collector temp
    * collector voltage
    * collector position
    * collector richardson
    * collector emissivity
    * emitter barrier
    * emitter temp
    * emitter voltage
    * emitter position
    * emitter richardson
    * emitter emissivity
    
    [1] https://github.com/mnielsen/neural-networks-and-deep-learning
    """
    electrodes = ("collector", "emitter")
    attributes = ("barrier", "temp", "voltage", "position", "richardson", "emissivity")
    
    abscissae = np.array([datum[electrode][attribute] for electrode, attribute in itertools.product(electrodes, attributes)])
    abscissae_matrix = np.ndarray(buffer=abscissae, shape=(12, 1))
    ordinate = datum["max_motive"]
    
    return (abscissae_matrix, ordinate)

with open("training_dicts.json", "r") as f:
    training_data_json = json.load(f)
    
with open("validation_dicts.json", "r") as f:
    validation_data_json = json.load(f)

training_data = [convert_dat(datum) for datum in training_data_json]
validation_data = [convert_dat(datum) for datum in validation_data_json]

hidden_nodess = [5, 50]
etas = [1e-2, 1., 10]

for hidden_nodes, eta in itertools.product(hidden_nodess, etas):
    print "=" * 30
    print "hidden nodes:", hidden_nodes
    print "eta:", eta
    net = network.Network([12, hidden_nodes, 1])
    start_time = time.time()
    net.SGD(training_data, 100, 10, 1e-3, test_data=validation_data)
    print time.time() - start_time
