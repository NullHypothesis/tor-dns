#!/bin/bash

Rscript plot-rounds.R 1kx100+100k.csv

pdfcrop rounds-1kx100+100k.pdf rounds-1kx100+100k.pdf
