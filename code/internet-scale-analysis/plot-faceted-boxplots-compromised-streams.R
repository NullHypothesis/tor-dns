require(ggplot2)
library(scales)
library(grid)


sampling_rate <- 100
output_file <- "compromised-streams.pdf"
cairo_pdf(output_file, height=2, width=5.7)

data <- data.frame()
for (dir_name in c("2856", "3215", "3320", "7922", "42610")) {

    # Read all files in directory.
    for (base_name in c("8888_comp_streams_",
                        "ddptr_comp_streams_",
                        "isps_comp_streams_",
                        "status_quo_comp_streams_")) {

        # Construct path and read CSV.
        file_name <- paste(base_name, dir_name, ".txt", sep = "")
        csv <- read.csv(paste(dir_name, file_name, sep = "/"), header = TRUE)

        # Add data to our data frame.
        data <- rbind(data, data.frame(x = csv$compromised / (csv$compromised + csv$noncompromised),
                                       isp = dir_name,
                                       setup = base_name,
                                       stringsAsFactors=FALSE))
    }
}

data[data$isp == "2856", "isp"] <- "UK"
data[data$isp == "3215", "isp"] <- "FR"
data[data$isp == "3320", "isp"] <- "DE"
data[data$isp == "7922", "isp"] <- "US"
data[data$isp == "42610", "isp"] <- "RU"

data[data$setup == "8888_comp_streams_", "setup"] <- "Google DNS only"
data[data$setup == "ddptr_comp_streams_", "setup"] <- "Local DNS only"
data[data$setup == "isps_comp_streams_", "setup"] <- "ISP DNS only"
data[data$setup == "status_quo_comp_streams_", "setup"] <- "Status quo"

ggplot(data, aes(isp, x)) +
    labs(x = "Tor client ISP") +
    labs(y = "Fraction of compromised streams") +
    geom_boxplot(outlier.shape = NA) +
    scale_y_continuous(breaks = c(0.0, 0.1, 0.2, 0.3, 0.4),
                       labels = c("0", "0.1", "0.2", "0.3", "0.4"),
                       limits = c(0, 0.4)) +
    coord_flip() +
    theme_minimal() +
    theme(axis.text = element_text(colour = "gray50"),
          axis.ticks = element_line(colour = "gray90"),
          axis.ticks.x = element_line(size = 0.25),
          axis.ticks.y = element_line(size = 0.25)) +
    facet_grid(. ~ setup)

warnings()

dev.off()
