library(ggplot2)

cairo_pdf("dns-exposure.pdf", height=2.3, width=3.7)

args <- commandArgs(trailingOnly = TRUE)
as16276 <- read.csv(args[1], header = TRUE)
as1653  <- read.csv(args[2], header = TRUE)
as29169 <- read.csv(args[3], header = TRUE)
as7922  <- read.csv(args[4], header = TRUE)
as99    <- read.csv(args[5], header = TRUE)

# Build data structure for plotting.
data <- data.frame()
data <- rbind(data, data.frame(x = as1653$exposure,
                               location = "AS 1653 (SE)"))
data <- rbind(data, data.frame(x = as16276$exposure,
                               location = "AS 16276 (FR)"))
data <- rbind(data, data.frame(x = as29169$exposure,
                               location = "AS 29169 (FR)"))
data <- rbind(data, data.frame(x = as7922$exposure,
                               location = "AS 7922 (US)"))
data <- rbind(data, data.frame(x = as99$exposure,
                               location = "AS 99 (US)"))

median(data$x)

ggplot(data, aes(location, x)) +
       labs(x = "Vantage point") +
       labs(y = "Exposure metrics λ") +
       geom_boxplot() +
       coord_flip() +
       theme_minimal() +
       theme(axis.text = element_text(colour = "gray50"),
             axis.ticks = element_line(colour = "gray90"),
             axis.ticks.x = element_line(size = 0.25),
             axis.ticks.y = element_line(size = 0.25)) +

warnings()

dev.off()
