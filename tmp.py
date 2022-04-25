#!/usr/bin/python3

DICT_VAR= {'best':100, 'good':70, 'meh':20, 'bad':5,
           'terrible':1, 'never':0}

import numpy as np

keys, weights = zip(*DICT_VAR.items())
weights = [100, 70, 20, 5, 1, 0]
keys = ['best', 'good', 'meh', 'bad', 'terrible', 'never']
print(keys)
print(weights)
probs = np.array(weights, dtype=float) / float(sum(weights))
sample_np = np.random.choice(keys, 100, p=probs)
sample = [str(val) for val in sample_np]

print(sample)