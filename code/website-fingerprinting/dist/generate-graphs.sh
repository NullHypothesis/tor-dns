#!/bin/bash

Rscript plot-dist.R 1kx100+100k.csv

pdfcrop dist-1kx100+100k.pdf dist-1kx100+100k.pdf
