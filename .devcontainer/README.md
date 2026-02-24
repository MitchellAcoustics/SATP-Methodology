# VS Code Dev Container Setup

This project is configured to run in a Docker-based development environment using VS Code Dev Containers.

## Quick Start

1. **Install Prerequisites:**
   - VS Code: https://code.visualstudio.com/
   - Docker Desktop: https://www.docker.com/products/docker-desktop
   - Remote - Containers extension: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

2. **Open in Dev Container:**
   - Open this repository in VS Code
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Select "Dev Containers: Open in Container"
   - VS Code will build the container and reconnect inside it

3. **Initial Setup:**
   - The container will automatically run `uv sync` on first launch
   - This installs all Python dependencies into `.venv/` inside the container
   - R packages specified in `devcontainer.json` will be installed
   - You're ready to work once the terminal is ready

## What's Inside

The dev container includes:

- **Python 3.12.5** with all project dependencies (rpy2, xarray, circumplex, soundscapy, etc.)
- **R 4.2+** with development libraries for rpy2 integration
- **Quarto** for document rendering and publishing
- **Jupyter** support for interactive notebooks
- **Git, uv, and development tools** pre-installed
- **Ruff** for Python linting and formatting
- **VS Code extensions** for Python, Jupyter, Quarto, R, Docker, and Git

## Environment

- **Working directory:** `/workspace` (mounted to your local project)
- **Python path:** Configured to use `.venv/bin/python`
- **Volumes:**
  - Cache volume for faster builds and package downloads
  - Virtual environment volume for persistence
  - Workspace mount for live editing

## Usage

### Run Python Code

```bash
python computation/your_script.py
```

### Jupyter Notebooks

1. Open `computation/SATP-Methodology.ipynb` in VS Code
2. Select "Run All" or run individual cells
3. The Jupyter kernel runs inside the container

### Quarto

Render and preview your Quarto documents:

```bash
quarto preview index.qmd
quarto render index.qmd --to html
```

### Install Additional Dependencies

To add new packages to your project:

```bash
uv add package_name
```

This updates `pyproject.toml` and `uv.lock`, which persist after container rebuild.

## R Packages

To install R packages automatically when the container starts, add them to `devcontainer.json`:

```json
"settings": {
    "r.packages": [
        "yaml",
        "ggplot2",
        "dplyr"
    ]
}
```

The packages will be installed during the `postCreateCommand` phase (runs automatically on first container build).

**Important:** R package compilation can take several minutes, especially for packages with C/C++ dependencies (e.g., `devtools`, `tidyverse`). Start with simple packages like `yaml`, `jsonlite`, or pure-R packages.

### Installing R Packages Manually

If a package fails to install during build or you want to add packages later:

```bash
# In the container terminal
Rscript -e 'install.packages("package_name")'
```

## Troubleshooting

### Container won't start

- Ensure Docker Desktop is running
- Check Docker logs: `docker logs satp-dev`
- Rebuild the container: `Dev Containers: Rebuild Container`

### Package installation fails

- Run `uv sync` manually: Open terminal in VS Code and run the command
- Check internet connection (some packages pull from GitHub)
- Clear cache if needed: `docker volume prune`

### R package installation times out

- R packages with C/C++ dependencies (devtools, tidyverse, etc.) can take 5-15 minutes to compile
- Monitor progress in VS Code's terminal during `postCreateCommand`
- If it fails, rebuild with fewer packages and add others manually later

### R integration issues

- Verify rpy2 loaded: `python -c "import rpy2; print(rpy2.__version__)"`
- Check R path: `which R` (should show `/usr/bin/R`)
- Check installed R packages: `Rscript -e 'library(yaml); print(packageVersion("yaml"))'`

### Jupyter kernel connection issues

- Restart VS Code Jupyter kernel: `Shift+Cmd+P` → "Jupyter: Restart Kernel"
- Reload VS Code window: `Cmd+R` (Mac) or `F5` (Windows/Linux)

## Container Management

### Access Terminal in Container

A terminal is automatically available in VS Code when connected to the container.

### Remove Container

From VS Code: `Dev Containers: Remove Container`

Or manually:

```bash
docker compose -f .devcontainer/docker-compose.yaml down -v
```

### Rebuild Container

Press `Shift+Cmd+P` → `Dev Containers: Rebuild Container` (cleans and rebuilds)

## Performance Notes

- The `.venv` is stored in a named volume for faster I/O on Docker Desktop
- Cache directory persists between builds to speed up package downloads
- Workspace is mounted with `:cached` for better performance on macOS
- R package compilation happens in the container (not on your host machine)

## Documentation

- **Dev Containers Docs:** https://code.visualstudio.com/docs/devcontainers/containers
- **Docker Compose:** https://docs.docker.com/compose/
- **uv Package Manager:** https://docs.astral.sh/uv/
- **Quarto:** https://quarto.org/docs/
- **R Package Installation:** https://cran.r-project.org/
