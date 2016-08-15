require(ggplot2)
library(scales)
library(grid)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("1kx100+100k-recall-ggplot2.pdf", height=2.4, width=2.8)
data <- read.csv(input_file, header=TRUE)

df <- data.frame(x = data$pct,
                 y = data$ctw,
                 Attack = "ctw")

df <- rbind(df, data.frame(x = data$pct,
                           y = data$hp,
                           Attack = "hp"))

df <- rbind(df, data.frame(x = data$pct,
                           y = data$kwf,
                           Attack = "kwf"))

ggplot(df, aes(x, y, colour = Attack,
                     linetype = Attack,
                     shape = Attack)) +
    geom_point(size=2.5) +
    geom_line() +
    theme_bw() +
    labs(x = "Percentage of exit bandwidth") +
    labs(y = "Recall") +
    theme(legend.key.width = unit(2, "line"),
          legend.justification = c(1, 0),
          legend.key.height = unit(0.8, "line"),
          legend.key = element_rect(colour = "transparent", fill = "transparent"),
          legend.background = element_rect(colour = "gray", fill = "white", size = 0.3),
          legend.position = c(1.05, -0.05)) +
    scale_color_brewer(palette = "Set1")

dev.off()
