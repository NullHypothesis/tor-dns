library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("dns-exposure.pdf", height=2.3, width=3.7)
data <- read.csv(input_file, header=TRUE)

qplot(data$exposure,
      stat = "ecdf",
      geom = "step",
      ylab="Fraction of observations",
      xlab="Exposure metric λ",
) + theme_minimal() +
    theme(axis.text = element_text(colour = "gray50"),
          axis.ticks = element_line(colour = "gray90"),
          axis.ticks.x = element_line(size = 0.25),
          axis.ticks.y = element_line(size = 0.25))

dev.off()
