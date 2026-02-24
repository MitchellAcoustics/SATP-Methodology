# R Package Installation Examples

This document shows how to configure R packages for automatic installation when the dev container starts.

## Configuration

R packages are specified in `.devcontainer/devcontainer.json` under:

```json
"settings": {
    "r.packages": [
        "package1",
        "package2",
        "package3"
    ]
}
```

The packages will be automatically installed during container creation via the `postCreateCommand`.

## Recommended Packages by Use Case

### Minimal Setup (Fast Installation)
```json
"r.packages": []
```
No packages installed. Install manually as needed in the container terminal.

### Data Science Essentials (Medium Installation Time)
```json
"r.packages": [
    "jsonlite",
    "tidyr",
    "dplyr"
]
```

### Scientific Computing (Slower Installation)
```json
"r.packages": [
    "yaml",
    "jsonlite",
    "stringr",
    "ggplot2"
]
```

### Full Environment (Longest Installation)
```json
"r.packages": [
    "devtools",
    "tidyverse",
    "rmarkdown",
    "shiny"
]
```

**Warning:** Some packages take 5-15 minutes to compile (especially those with C/C++ dependencies like `devtools`, `tidyverse`).

## Installation Time Guide

**Fast (< 2 minutes):**
- `jsonlite`
- `curl`
- `stringr`

**Medium (2-5 minutes):**
- `yaml`
- `ggplot2`
- `dplyr`
- `reshape2`

**Slow (5-15+ minutes):**
- `devtools`
- `tidyverse`
- `rmarkdown`
- `data.table`

## Installation Process

1. Edit `devcontainer.json` and add your packages to `r.packages`
2. Rebuild the dev container: `Dev Containers: Rebuild Container`
3. VS Code will show progress in the terminal (look for "Installing R packages..." message)
4. Once complete, packages are available in the R environment

## Troubleshooting Installation

### Installation Fails

If a package fails to install:
1. Check the error message in VS Code's terminal
2. Most common causes: network issues, missing system dependencies, or incompatible package versions
3. Try installing the package manually in the container:
   ```bash
   Rscript -e 'install.packages("package_name")'
   ```

### Installation Takes Too Long

- Building from source can take 5-15 minutes per package
- Consider reducing the number of packages
- Use binary packages when available (usually happens automatically on recent R versions)

### Package Still Not Installed

After container is ready, verify installation manually:
```bash
Rscript -e 'library(yaml); cat("yaml installed!\n")'
```

## Manual Installation (Without Rebuild)

If you want to add packages without rebuilding:

```bash
# Inside container terminal
Rscript -e 'install.packages("new_package")'

# Or using R directly
R
> install.packages("new_package")
> q()
```

## Current Configuration

Your current `devcontainer.json` specifies:

```json
"r.packages": [
    "yaml"
]
```

To change this, edit `.devcontainer/devcontainer.json` directly and rebuild the container.
