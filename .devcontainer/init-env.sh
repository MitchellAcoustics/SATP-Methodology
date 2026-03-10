uv sync
Rscript -e 'install.packages("renv")'
Rscript -e 'renv::restore(prompt=FALSE)'
# Rscript -e 'tinytex::install_tinytex()'
source .venv/bin/activate
quarto check