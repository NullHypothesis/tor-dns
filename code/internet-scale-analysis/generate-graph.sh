#!/bin/bash

source ../config.sh

cd simulations-2016-08-16/
Rscript ../plot-faceted-boxplots-compromised-streams.R
Rscript ../plot-faceted-boxplots-time-until-compromise.R

pdfcrop compromised-streams.pdf \
        compromised-streams.pdf

pdfcrop time-until-compromise.pdf \
        time-until-compromise.pdf

cp compromised-streams.pdf time-until-compromise.pdf \
   "$FIGURES_DIR"
