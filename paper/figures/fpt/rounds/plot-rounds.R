# Create a plot by running:
#
#   Rscript plot-rounds.R FILE
#
# The plot is then written to "rounds.pdf".

require(ggplot2)
library(scales)
library(grid)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("1kx100+100k-ggplot2.pdf", height=2.6, width=3)
data <- read.csv(input_file, header=TRUE)

df <- data.frame(x = data$r,
                 y = data$ctw,
                 Attack = "ctw")

df <- rbind(df, data.frame(x = data$r,
                           y = data$hp,
                           Attack = "hp"))

df <- rbind(df, data.frame(x = data$r,
                           y = data$wf,
                           Attack = "wf"))

ggplot(df, aes(x, y, colour = Attack,
                     linetype = Attack,
                     shape = Attack)) +
    geom_point(size=2.5) +
    geom_line() +
    theme_bw() +
    labs(x = "Weight learning rounds") +
    labs(y = "Precision") +
    theme(legend.key.width = unit(2, "line"),
          legend.justification = c(1, 0),
          legend.key.height = unit(0.8, "line"),
          legend.key = element_rect(colour = "transparent", fill = "transparent"),
          legend.background = element_rect(colour = "gray", fill = "white", size = 0.3),
          legend.position = c(1.05, -0.05)) +
    scale_color_brewer(palette = "Set1") +
    scale_x_continuous(labels = comma)

dev.off()
