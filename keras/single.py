#!/usr/bin/env python3.5
import sys, pickle, os

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams.update({'font.size': 36})

import random

from .generate import generate_with
from .functions import functions
from .sieve import gen_primes, gen_composites, take

def unpair(paired):
    A = []
    B = []
    for a, b in paired:
        A.append(a)
        B.append(b)
    return A, B

maxbits = 256

to_binary_list  = lambda n : list(map(int, bin(n)[2:]))
pad_binary_list = lambda l : [0] * (maxbits - len(l)) + l

def binary(n):
    return pad_binary_list(to_binary_list(n))

def run_nn_test(f, N, train_p, representation, randomize=True, epochs=5):
    data = generate_with(f, N)
    if randomize:
        random.shuffle(data)

    if representation == 'binary':
        data = [(binary(n), label) for n, label in data]

    split = int(N*train_p)

    train_ns, train_labels = unpair(data[:split])
    test_ns,  test_labels  = unpair(data[split:])

    train_ns     = np.array(train_ns)
    train_labels = np.array(train_labels)
    test_ns      = np.array(test_ns)
    test_labels  = np.array(test_labels)

    N_middle_layers = 10
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=((maxbits,) if representation == 'binary' else (1,)))] +
        [keras.layers.Dense(256, activation=tf.nn.relu)] * N_middle_layers + [
        keras.layers.Dense(2, activation=tf.nn.softmax)
    ])

    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_ns, train_labels, epochs=epochs)
    test_loss, test_acc = model.evaluate(test_ns, test_labels)
    return test_acc

power = 2
train_p = 0.5
representation = 'binary'
#representation = 'decimal'
start = 2
end = 8

def plot_accuracies(accuracies):
    accuracies = accuracies.pivot(index='datapoints', columns='name', values='accuracies')
    order = sorted(accuracies.columns.values, key=lambda k : sum(accuracies[k]))
    accuracies = accuracies[list(order)]
    sns.set(rc={'figure.figsize':(6,3.5)}, font_scale=1.8)
    sns.heatmap(accuracies, annot=True, vmin=0.0, vmax=1.0)
    plt.xlabel('Sequences')
    plt.ylabel('Total data points (trained on half)')
    plt.title('Accuracies as a function of number of datapoints per sequence')
    plt.show()

def nn_test(f, N):
    return run_nn_test(f, N, train_p, representation, randomize=True, epochs=15)

def generate_accuracies(test):
    accuracies = dict(datapoints=[], accuracies=[], name=[])
    for name in list(functions.keys()):
        print('Learning ' + name)
        for i in range(start, end):
            N = power ** i

            f = functions[name]
            test_acc = test(f, N)

            accuracies['datapoints'].append(N)
            accuracies['accuracies'].append(test_acc)
            accuracies['name'].append(name)
    return accuracies

def main(args):
    if not os.path.isfile('keras_accuracies.pkl'):
        accuracies = generate_accuracies(nn_test)
        accuracies = pandas.DataFrame(accuracies)
        with open('keras_accuracies.pkl', 'wb') as infile:
            pickle.dump(accuracies, infile)
    else:
        with open('keras_accuracies.pkl', 'rb') as infile:
            accuracies = pickle.load(infile)
    plot_accuracies(accuracies)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
