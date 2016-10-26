#!/bin/bash

source ../config.sh

Rscript plot-exposure.R \
    top-1k-ddptr-2016-10-25-as16276.csv \
    top-1k-ddptr-2016-10-25-as1653.csv \
    top-1k-ddptr-2016-10-25-as29169.csv \
    top-1k-ddptr-2016-10-25-as7922.csv \
    top-1k-ddptr-2016-10-25-as99.csv

pdfcrop dns-exposure.pdf \
        dns-exposure.pdf

cp dns-exposure.pdf "$FIGURES_DIR"
