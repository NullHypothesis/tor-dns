#!/bin/bash

Rscript alexa-precision.R 1kx100+100k-precision.csv
Rscript alexa-recall.R    1kx100+100k-recall.csv

pdfcrop 1kx100+100k-precision-ggplot2.pdf 1kx100+100k-precision-ggplot2.pdf
pdfcrop 1kx100+100k-recall-ggplot2.pdf    1kx100+100k-recall-ggplot2.pdf
