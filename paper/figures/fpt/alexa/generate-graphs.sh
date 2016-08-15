#!/bin/bash

Rscript alexa-precision.R 1kx100+100k-offsets-100pct-precision.csv
Rscript alexa-recall.R    1kx100+100k-offsets-100pct-recall.csv

pdfcrop 1kx100+100k-offsets-100pct-precision-ggplot2.pdf 1kx100+100k-offsets-100pct-precision-ggplot2.pdf
pdfcrop 1kx100+100k-offsets-100pct-recall-ggplot2.pdf    1kx100+100k-offsets-100pct-recall-ggplot2.pdf
