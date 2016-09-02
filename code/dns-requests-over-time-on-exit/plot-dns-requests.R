require(ggplot2)
library(scales)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("dns-requests.pdf", height=2.3, width=5.5)
data <- read.csv(input_file, header=TRUE)

data$timestamp <- as.POSIXct(data$timestamp, origin="1970-01-01")

# Subset only one representative day worth of data.
data <- subset(data, timestamp > as.POSIXct("2016-05-25") & timestamp < as.POSIXct("2016-05-26"))

ggplot(data, aes(timestamp, count)) +
    geom_area() +
    scale_x_datetime(labels = date_format("%H:%M\n%b %d")) +
    labs(x = "Time") +
    labs(y = "DNS requests per\nfive minutes") +
    theme_minimal() +
    theme(axis.text = element_text(colour = "gray50"),
          axis.ticks = element_line(colour = "gray90"),
          axis.ticks.x = element_line(size = 0.25),
          axis.ticks.y = element_line(size = 0.25))

dev.off()
