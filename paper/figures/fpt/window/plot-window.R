require(ggplot2)
library(scales)
library(grid)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("1kx100+100k-ggplot2.pdf", height=2.6, width=3)
data <- read.csv(input_file, header=TRUE)

df <- data.frame(x = data$window / 60,
                 y = data$ctw10k,
                 Attack = "ctw-10k")

df <- rbind(df, data.frame(x = data$window / 60,
                           y = data$hp10k,
                           Attack = "hp-10k"))

df <- rbind(df, data.frame(x = data$window / 60,
                           y = data$wf10k,
                           Attack = "wf-10k"))

df <- rbind(df, data.frame(x = data$window / 60,
                           y = data$ctw100k,
                           Attack = "ctw-100k"))

df <- rbind(df, data.frame(x = data$window / 60,
                           y = data$hp100k,
                           Attack = "hp-100k"))

df <- rbind(df, data.frame(x = data$window / 60,
                           y = data$wf100k,
                           Attack = "wf-100k"))

ggplot(df, aes(x, y, colour = Attack,
                     linetype = Attack,
                     shape = Attack)) +
    geom_point(size=2.5) +
    geom_line() +
    theme_bw() +
    labs(x = "Window size (minutes)") +
    labs(y = "Precision") +
    ylim(0.65, 1) +
    theme(legend.key.width = unit(2, "line"),
          legend.justification = c(1, 0),
          legend.position = c(1.03, -0.05),
          legend.key.height = unit(0.8, "line"),
          legend.background = element_rect(colour = "gray", fill = "white", size = 0.3),
          legend.key = element_rect(colour = "transparent", fill = "transparent")) +
    scale_color_brewer(palette = "Dark2") +
    guides(col=guide_legend(ncol=2))

dev.off()
