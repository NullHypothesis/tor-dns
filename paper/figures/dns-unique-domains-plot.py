#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import normal
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
import random
import csv
import sys

def get_data(path):
    names = []
    with open(path) as f:
        fl = f.readline()
        names = fl.rstrip().split(',')[1:]
    v_hist = np.ravel(np.recfromcsv(path,delimiter=',',comments='#'))
    x = [ t for t in zip(*v_hist) ]
    return x[0], x[1:], names

if __name__ == '__main__':
    fig, ax = plt.subplots()
    data, output = sys.argv[1], sys.argv[2]
    alexa, d, names = get_data(data)

    # see http://matplotlib.org/api/lines_api.html
    linestyles = ["-.", "-", ":", "--", "-.", "-", ":", "--"]
    markerstyles = ['o', 'v', '^', '<', '>', '8',
    's', 'p', '*', 'h', 'H', 'D', 'd']
    ax.set_prop_cycle(cycler('color', ['c', 'm', 'y', 'k',
    'tomato', 'lightskyblue', 'limegreen', 'chocolate']))

    for j in xrange(len(d)):
        plot(alexa, d[j], label=names[j], ls=linestyles[j],
         marker=markerstyles[j], markersize=8, lw=1)

    plt.xlabel('Alexa top one million (log scale)', labelpad=7.0, fontsize=16)
    plt.ylabel('Frac. unique domain(s)', labelpad=9.0, fontsize=16)
    plt.grid()
    plt.ylim(0, 1)
    #plt.legend(prop={'size':12}, loc=4, ncol=2)
    ax.set_xscale('log', basex=10)
    plt.xticks([ pow(10,i) for i in range(1,7) ])
    fig.set_size_inches(6,3)
    plt.tight_layout()

    if output in ['--pdf','--png','--svg']:
        plt.savefig( "{}.{}".format(data[:-4],output[2:]), dpi=400, format=output[2:])
    elif output == '--show':
        plt.show()
    else:
        print "Unsupported output format."
