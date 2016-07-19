#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import normal
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
import random
from itertools import cycle
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
    data, ymin, output = sys.argv[1], sys.argv[2], sys.argv[3]
    lengths, d, names = get_data(data)

    # see http://matplotlib.org/api/lines_api.html
    linestyles = cycle(["-.", "-", ":", "--", "-.", "-", ":", "--"])
    markerstyles = cycle(['o', 'v', '^', '<', '>', '8',
    's', 'p', '*', 'h', 'H', 'D', 'd'])
    ax.set_prop_cycle(cycler('color', ['c', 'm', 'y', 'k',
    'tomato', 'lightskyblue', 'limegreen', 'chocolate']))

    for j in xrange(len(d)):
        plot(lengths, d[j], label=names[j], ls=next(linestyles),
         marker=next(markerstyles), markersize=10, lw=1)

    plt.xlabel('monitored sites Alexa rank', labelpad=7.0, fontsize=16)
    plt.ylabel('recall', labelpad=9.0, fontsize=16)
    plt.grid()
    plt.ylim(float(ymin), 1)
    ax.set_xscale('log', basex=10)
    plt.xticks([ pow(10,i) for i in range(1,7) ])
    plt.legend(prop={'size':12}, loc=2, ncol=2)
    fig.set_size_inches(5,4)
    plt.tight_layout()

    if output in ['--pdf','--png','--svg']:
        plt.savefig( "{}.{}".format(data[:-4],output[2:]), dpi=400, format=output[2:])
    elif output == '--show':
        plt.show()
    else:
        print "Unsupported output format."
