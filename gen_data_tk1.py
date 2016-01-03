# -*- coding: utf-8 -*-

import itertools
import time
import json
import sys
import tec
import numpy as np

em_params = {"temp": 1000.,
             "barrier": 2.,
             "richardson": 10., }

co_params = {"temp": 300.,
             "barrier": 1.,
             "richardson": 10.,
             "position": 10., }

emitter_temps = [("emitter", "temp", val) for val in np.linspace(300, 2000, 5)]
emitter_barriers = [("emitter", "barrier", val) for val in np.linspace(1, 4, 10)]
collector_barriers = [("collector", "barrier", val) for val in np.linspace(1, 4, 5)]
collector_voltages = [("collector", "voltage", val) for val in np.linspace(0, 2, 20)]
collector_positions = [("collector", "position", val) for val in np.linspace(1, 10, 2)]

# There's a better way to do this with iterators
data = []

start_time = time.time()
for itr in itertools.product(emitter_temps, emitter_barriers, collector_barriers, collector_voltages, collector_positions):
    # Construct dictionaries out of the combination of parameters
    em_dict = dict([itm[1:] for itm in itr if itm[0] == "emitter"])
    co_dict = dict([itm[1:] for itm in itr if itm[0] == "collector"])
    
    # Update the dictionaries used to initialize the TEC electrodes
    em_params = dict(em_params.items() + em_dict.items())
    co_params = dict(co_params.items() + co_dict.items())
    
    # Create electrodes and `Langmuir` objects
    em = tec.electrode.Metal.from_dict(em_params)
    co = tec.electrode.Metal.from_dict(co_params)
    
    data.append(tec.models.Langmuir(em, co))

print "Initialization time for list of Langmuir objects:"
print time.time() - start_time

start_time = time.time()
with open("data_tk1.json", "w") as f:
    f.write(json.dumps(data, default=tec.io.to_json, indent=4))

print "Write time of JSON formatted file:"
print time.time() - start_time

print "Length of data array:"
print len(data)
print "Size of data array in memory"
print sys.getsizeof(data)
