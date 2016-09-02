#!/bin/bash

source ../config.sh

Rscript plot-resolvers-of-exits.R asn-bw-frac.csv
pdfcrop asn-bw-frac.pdf \
        asn-bw-frac.pdf

cp asn-bw-frac.pdf "$FIGURES_DIR"
