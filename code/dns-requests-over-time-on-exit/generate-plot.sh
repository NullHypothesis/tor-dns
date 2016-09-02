#!/bin/bash

source ../config.sh

Rscript plot-dns-requests.R 2016-05-15-to-2016-05-31-80-and-443.csv
pdfcrop dns-requests.pdf \
        dns-requests.pdf

cp dns-reqs.pdf "$FIGURES_DIR"
