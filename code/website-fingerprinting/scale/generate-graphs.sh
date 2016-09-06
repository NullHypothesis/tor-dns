#!/bin/bash

Rscript plot-scale.R 1kx100+100k.csv

pdfcrop scale-1kx100+100k.pdf scale-1kx100+100k.pdf
