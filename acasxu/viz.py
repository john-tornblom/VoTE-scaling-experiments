#!/usr/bin/env python
import os
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

import nnet
import vote


colors = [(0.9, 0.9, 0.9, 1),
          (0.5, 0.5, 0.5, 1), (0.7, 0.7, 0,1),
          (0, 0, 0.5, 1), (0, 0.6, 0, 1), ]

    
def render_prediction(ax, predict, rect=False, psi=np.pi, v_own=200, v_int=200):
    L = []
    X = []
    Y = []
    for x in np.arange(-30000, 30000, 201):
        for y in np.arange(-10000, 10000, 201):
            if rect:
                inputs = [x, y, psi, v_own, v_int]
            else:
                rho = np.sqrt(x ** 2 + y **2)
                theta = np.arctan(y / x)
                inputs = [rho, theta, psi, v_own, v_int]

            outputs = predict(inputs)
            label = np.argmin(outputs)
            
            X.append(x / 1000)
            Y.append(y / 1000)
            L.append(label)

    return ax.scatter(X, Y, c=L, cmap=ListedColormap(colors))


if __name__ == '__main__':

    font = {'family' : 'sans',
            'size'   : 16}

    plt.rc('font', **font)

    filename = '%s/nnet/ACASXU_run2a_1_1_batch_2000.nnet' % (
        os.path.dirname(__file__) or '.'
    )
    nn = nnet.NeuralNetwork(filename, True, True)

    filename = '%s/models/ACASXU_1_1.json' % (os.path.dirname(__file__) or '.')
    gbm = vote.Ensemble.from_file(filename)

    fig, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)

    render_prediction(ax1, nn.evaluate)
    render_prediction(ax2, lambda xvec: gbm.eval(*xvec))

    legend_elements = [Patch(color=colors[0], label='COC'),
                       Patch(color=colors[1], label='WL'),
                       Patch(color=colors[2], label='WR'),
                       Patch(color=colors[3], label='SL'),
                       Patch(color=colors[4], label='SR')]

    fig.legend(handles=legend_elements,
               loc='center right',
               borderaxespad=0.1,
               title='Advisories')
    
    plt.xlabel('Downrange (kft)')
    plt.ylabel('Crossrange (kft)')
    ax1.set_ylabel('Crossrange (kft)')
    
    #plt.title()
    fig = plt.show()
