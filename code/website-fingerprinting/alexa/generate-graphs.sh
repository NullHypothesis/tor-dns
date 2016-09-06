#!/bin/bash

Rscript alexa-precision.R 1kx100+100k-precision.csv
Rscript alexa-recall.R    1kx100+100k-recall.csv

pdfcrop alexa-1kx100+100k-precision.pdf alexa-1kx100+100k-precision.pdf
pdfcrop alexa-1kx100+100k-recall.pdf    alexa-1kx100+100k-recall.pdf
