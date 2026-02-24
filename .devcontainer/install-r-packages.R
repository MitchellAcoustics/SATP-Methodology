#!/usr/bin/env Rscript
# Install R packages specified as command-line arguments
# Usage: Rscript install-r-packages.R package1 package2 package3

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  cat("No packages specified. Skipping R package installation.\n")
  quit(status = 0)
}

cat("Installing R packages:", paste(args, collapse = ", "), "\n")

# Set up package installation
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Install packages
install.packages(args, dependencies = TRUE, quiet = FALSE)

cat("R package installation complete.\n")
