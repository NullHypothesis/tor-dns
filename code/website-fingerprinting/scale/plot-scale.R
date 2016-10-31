require(ggplot2)
library(scales)
library(grid)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("scale-1kx100+100k.pdf", height=2.6, width=3)
data <- read.csv(input_file, header=TRUE)

df <- data.frame(x = data$scale,
                 y = data$ctw10k,
                 Attack = "ctw-10k")

df <- rbind(df, data.frame(x = data$scale,
                           y = data$hp10k,
                           Attack = "hp-10k"))

df <- rbind(df, data.frame(x = data$scale,
                           y = data$wf10k,
                           Attack = "wf-10k"))

df <- rbind(df, data.frame(x = data$scale,
                           y = data$ctw100k,
                           Attack = "ctw-100k"))

df <- rbind(df, data.frame(x = data$scale,
                           y = data$hp100k,
                           Attack = "hp-100k"))

df <- rbind(df, data.frame(x = data$scale,
                           y = data$wf100k,
                           Attack = "wf-100k"))

ggplot(df, aes(x, y, colour = Attack,
                     linetype = Attack,
                     shape = Attack)) +
    geom_point(size=2.5) +
    geom_line() +
    theme_minimal() +
    ylim(0.63, 1) +
    labs(x = "Tor network scale") +
	scale_x_continuous(breaks=c(0,1,2,4,6,8,10)) +
    geom_vline(xintercept = 1, alpha=0.5) +
    labs(y = "Precision") +
    theme(legend.key.width = unit(2, "line"),
          legend.justification = c(1, 0),
          legend.position = c(1.04, -0.05),
          legend.key.height = unit(0.8, "line"),
          legend.background = element_rect(colour = "gray", fill = "white", size = 0.3),
          legend.key = element_rect(colour = "transparent", fill = "transparent"),
          axis.text = element_text(colour = "gray50"),
          axis.ticks = element_line(colour = "gray90"),
          axis.ticks.x = element_line(size = 0.25),
          axis.ticks.y = element_line(size = 0.25)) +
    scale_color_brewer(palette = "Dark2") +
    guides(col=guide_legend(ncol=2))

dev.off()
