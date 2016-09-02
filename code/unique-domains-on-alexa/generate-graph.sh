#!/bin/bash

source ../config.sh

./binnify.py uniquecount.csv > uniquecount-binned.csv

Rscript plot-unique-domains.R uniquecount-binned.csv
pdfcrop dns-unique-domains.pdf dns-unique-domains.pdf
cp dns-unique-domains.pdf "$FIGURES_DIR"
