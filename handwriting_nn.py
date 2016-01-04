# Code adapted from "Neural Networks and Deep Learning" by Nielsen.

import mnist_loader
import network
import time

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
net = network.Network([784, 30, 10])

start_time = time.time()
net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
print time.time() - start_time
