library(ggplot2)
library(scales)
library(grid)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

cairo_pdf("asn-bw-frac.pdf", height=2.3, width=11)
data <- read.csv(input_file, header=TRUE)
data$time <- as.POSIXct(paste(data$time), format="%Y-%m-%dT%H:%M:%SZ")
data$time <- as.Date(data$time)

df <- data.frame(x = data$time,
                 y = data$as15169,
                 Resolver = "Google")
df <- rbind(df, data.frame(x = data$time,
                           y = data$as0,
                           Resolver = "Local"))
df <- rbind(df, data.frame(x = data$time,
                           y = data$as16276,
                           Resolver = "OVH"))
# df <- rbind(df, data.frame(x = data$time,
#                            y = data$as3356,
#                            Resolver = "Level 3"))
# df <- rbind(df, data.frame(x = data$time,
#                            y = data$as9008,
#                            Resolver = "Visual Online"))
# df <- rbind(df, data.frame(x = data$time,
#                            y = data$as13030,
#                            Resolver = "Init7"))
df <- rbind(df, data.frame(x = data$time,
                           y = data$as36692,
                           Resolver = "OpenDNS"))
# df <- rbind(df, data.frame(x = data$time,
#                            y = data$as37560,
#                            Resolver = "Cyberdyne"))
# df <- rbind(df, data.frame(x = data$time,
#                            y = data$as43350,
#                            Resolver = "NFOrce Entertainment"))
# df <- rbind(df, data.frame(x = data$time,
#                            y = data$as60781,
#                            Resolver = "LeaseWeb"))

ggplot(df, aes(x, y, colour = Resolver,
                     linetype = Resolver,
                     shape = Resolver)) +
    geom_point(size = 2) +
    geom_line() +
    labs(x = "Time") +
    labs(y = "Fraction of\nexit bandwidth") +
    scale_x_date(breaks = "1 month",
                 minor_breaks = "1 week",
                 labels=date_format("%b %Y")) +
    theme(legend.key.width = unit(2, "line"),
          legend.key = element_blank()) +
    scale_color_brewer(palette="Set1") +
    theme_minimal() +
    theme(axis.text = element_text(colour = "gray50"),
          axis.ticks = element_line(colour = "gray90"),
          axis.ticks.x = element_line(size = 0.25),
          axis.ticks.y = element_line(size = 0.25),
          legend.key.width = unit(1, "cm"))

dev.off()
