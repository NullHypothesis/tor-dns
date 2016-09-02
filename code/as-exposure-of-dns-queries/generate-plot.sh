#!/bin/bash

source ../config.sh

Rscript plot-exposure.R top-1k-ddptr-2016-04-19-ovh.csv
pdfcrop dns-exposure.pdf \
        dns-exposure.pdf

cp dns-exposure.pdf "$FIGURES_DIR"
