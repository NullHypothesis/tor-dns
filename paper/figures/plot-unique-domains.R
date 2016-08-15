# Create a plot by running:
#
#   Rscript plot-unique-domains.R dns-unique-domains.csv
#
# The plot is then written to "unique-domains.pdf".

require(ggplot2)
library(scales)
library(grid)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("dns-unique-domains.pdf", height=2.4, width=4.5)
data <- read.csv(input_file, header=TRUE)

ggplot(data, aes(alexatopX, fraction)) +
    geom_point(size=2.5) +
    geom_line() +
    theme_bw() +
    labs(x = "Alexa top one million (log)") +
    labs(y = "Frac. of unique domains") +
    scale_x_continuous(trans = "log10",
                       breaks = trans_breaks("log10", function(x) 10^x),
                       labels = trans_format("log10", math_format(10^.x)))

dev.off()
