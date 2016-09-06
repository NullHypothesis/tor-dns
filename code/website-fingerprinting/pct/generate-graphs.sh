#!/bin/bash

Rscript pct-precision.R 1kx100+100k-precision.csv
Rscript pct-recall.R    1kx100+100k-recall.csv

pdfcrop pct-1kx100+100k-precision.pdf pct-1kx100+100k-precision.pdf
pdfcrop pct-1kx100+100k-recall.pdf    pct-1kx100+100k-recall.pdf
