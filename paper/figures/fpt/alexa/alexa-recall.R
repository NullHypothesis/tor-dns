require(ggplot2)
library(scales)
library(grid)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("1kx100+100k-offsets-100pct-recall-ggplot2.pdf", height=2.4, width=2.8)
data <- read.csv(input_file, header=TRUE)

df <- data.frame(x = data$offset,
                 y = data$ctw,
                 Attack = "ctw")

df <- rbind(df, data.frame(x = data$offset,
                           y = data$hp,
                           Attack = "hp"))

df <- rbind(df, data.frame(x = data$offset,
                           y = data$wf,
                           Attack = "wf"))

ggplot(df, aes(x, y, colour = Attack,
                     linetype = Attack,
                     shape = Attack)) +
    geom_point() +
    geom_line() +
    theme_bw() +
    labs(x = "Alexa site rank") +
    labs(y = "Recall") +
    theme(legend.key.width = unit(2, "line"),
          legend.justification = c(1, 0),
          legend.key = element_rect(colour = "transparent", fill = "transparent"),
          legend.background = element_rect(colour = "gray", fill = "white", size = 0.3),
          legend.key.height = unit(0.8, "line"),
          legend.position = c(0.5, 0.4)) +
    ylim(0.52, 0.65) +
    scale_color_brewer(palette = "Set1") +
    scale_x_continuous(trans = "log10",
                       breaks = trans_breaks("log10", function(x) 10^x),
                       labels = trans_format("log10", math_format(10^.x)))

dev.off()
