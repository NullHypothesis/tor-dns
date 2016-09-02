require(ggplot2)
library(scales)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("dns-unique-domains.pdf", height=2.3, width=3.8)
data <- read.csv(input_file, header=TRUE)

ggplot(data, aes(site, uniqueCount)) +
    geom_point(size=1, alpha=1/2) +
    # geom_smooth(method="lm", formula=y~log(x), color="red") +
    labs(x = "Alexa top one million in bins of 1,000") +
    labs(y = "Fraction of web sites\nwith unique domains") +
    scale_x_continuous(labels = comma) +
    # Highlight outlier.
    annotate("text", x = 180000, y = 0.785, label = "Top 1,000 sites", size = 3) +
    theme_minimal() +
    theme(axis.text = element_text(colour = "gray50"),
          axis.ticks = element_line(colour = "gray90"),
          axis.ticks.x = element_line(size = 0.25),
          axis.ticks.y = element_line(size = 0.25))

dev.off()
