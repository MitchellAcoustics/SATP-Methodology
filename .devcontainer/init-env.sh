#!/usr/bin/env bash
set -euo pipefail

uv sync
Rscript -e 'install.packages(c("renv@1.1.5", "yaml"), repos = "https://cloud.r-project.org")'
Rscript -e 'renv::restore(packages = "renv", prompt=FALSE)'
Rscript -e 'renv::restore(prompt=FALSE)'
# Rscript -e 'tinytex::install_tinytex()'
source .venv/bin/activate
quarto check