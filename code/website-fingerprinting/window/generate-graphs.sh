#!/bin/bash

Rscript plot-window.R 1kx100+100k.csv

pdfcrop window-1kx100+100k.pdf window-1kx100+100k.pdf
