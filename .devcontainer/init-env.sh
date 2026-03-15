#!/usr/bin/env bash
set -euo pipefail

uv sync
Rscript -e 'if (!"renv" %in% rownames(installed.packages())) install.packages("renv", repos = "https://cloud.r-project.org")'
Rscript -e 'renv::restore(prompt=FALSE)'
# Rscript -e 'tinytex::install_tinytex()'
source .venv/bin/activate
quarto check