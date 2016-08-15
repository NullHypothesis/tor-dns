#!/bin/bash

Rscript pct-precision.R 1kx100+100k-precision.csv
Rscript pct-recall.R    1kx100+100k-recall.csv

pdfcrop 1kx100+100k-precision-ggplot2.pdf 1kx100+100k-precision-ggplot2.pdf
pdfcrop 1kx100+100k-recall-ggplot2.pdf    1kx100+100k-recall-ggplot2.pdf
