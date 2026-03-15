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
   - The container will automatically run `uv sync` to install Python dependencies (specified in `pyproject.toml`)
   - Then `renv::restore()` to install all R packages from `renv.lock`
   - R packages install in parallel using pak for speed
   - You're ready to work once the terminal is ready

## What's Inside

The dev container includes:

- **uv** package manager for Python environment and dependency management
- **Python** version managed by uv based on `pyproject.toml` requirements
- **R 4.4.2** with development libraries for rpy2 integration
- **renv** for reproducible R package management with pak for fast installation
- **Quarto** for document rendering and publishing
- **Jupyter** support for interactive notebooks
- **Git, development tools, and system libraries** pre-installed
- **Ruff** for Python linting and formatting
- **VS Code extensions** for Python, Jupyter, Quarto, R, Docker, and Git

## Customizing R Version

To use a different R version, edit `.devcontainer/docker-compose.yaml`:

```yaml
build:
  args:
    R_VERSION: "4.4.2"
```

Then rebuild: `Dev Containers: Rebuild Container`

**Available R versions:** Any version available from the Rocker project (e.g., `4.1.3`, `4.2.2`, `4.3.1`, `4.4.2`)

Check available versions at: https://hub.docker.com/r/rocker/r-ver/tags

## Python Version Management

Python version is automatically managed by **uv** based on your `pyproject.toml`. To change Python versions:

1. Edit `pyproject.toml` and update the `requires-python` field:
   ```toml
   requires-python = ">=3.11"
   ```

2. Run `uv sync` in the container to install the appropriate Python version

uv handles downloading and managing the exact Python version you need.

## Environment

- **Working directory:** `/workspace` (mounted to your local project)
- **Python path:** Managed by uv (typically `/root/.local/share/uv/pythons/`)
- **R path:** `/usr/local/bin/R`
- **Volumes:**
  - Cache volume for faster builds and package downloads
  - Virtual environment volume for persistence
  - renv cache volume for R package caching
  - pak cache volume for R package binary caching
  - Workspace mount for live editing

## Usage

### Run Python Code

```bash
uv run python computation/your_script.py
```

Or activate the virtual environment:

```bash
source .venv/bin/activate
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

### Install Additional Python Dependencies

To add new packages to your project:

```bash
uv add package_name
```

This updates `pyproject.toml` and `uv.lock`, which persist after container rebuild.

### Install Additional R Packages

To add R packages, use renv inside the container:

```bash
R
> renv::install("package_name")
> q()
```

This updates `renv.lock` automatically. Packages install in parallel using pak for speed.

See [R_PACKAGES.md](./R_PACKAGES.md) for detailed R package management.

## Troubleshooting

### Container won't start

- Ensure Docker Desktop is running
- Check Docker logs: `docker logs satp-dev`
- Rebuild the container: `Dev Containers: Rebuild Container`

### Python sync fails

- Run `uv sync` manually in the container terminal
- Check `pyproject.toml` for syntax errors
- Check internet connection (uv downloads Python from astral.sh)
- Clear uv cache: `uv cache clean`

### R package restoration fails

- Check the error in VS Code's terminal during `postCreateCommand`
- Most issues are missing system libraries (Dockerfile has common ones pre-installed)
- Try manual installation: `Rscript -e 'renv::install("package_name")'`
- See [R_PACKAGES.md](./R_PACKAGES.md) for troubleshooting

### R integration issues

- Verify rpy2 loaded: `python -c "import rpy2; print(rpy2.__version__)"`
- Check R path: `which R` (should show `/usr/local/bin/R`)
- Check renv status: `Rscript -e 'renv::status()'`
- Check R version: `R --version`

### Jupyter kernel connection issues

- Restart VS Code Jupyter kernel: `Shift+Cmd+P` → "Jupyter: Restart Kernel"
- Reload VS Code window: `Cmd+R` (Mac) or `F5` (Windows/Linux)

### Version mismatch after changing R version

If you change the R version in `docker-compose.yaml`, rebuild completely:
1. `Dev Containers: Remove Container`
2. `Dev Containers: Open in Container` (will rebuild fresh)

Or manually:
```bash
docker compose -f .devcontainer/docker-compose.yaml down -v
```

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

- Uses Rocker pre-compiled R binaries (fast builds, no compilation)
- uv downloads and caches Python versions efficiently
- The `.venv` is stored in a named volume for faster I/O on Docker Desktop
- R packages cached in `renv-cache` volume for speedy rebuilds
- Python cache directory persists between builds to speed up package downloads
- renv uses **pak** for parallel package installation (significantly faster than sequential)
- Workspace is mounted with `:cached` for better performance on macOS

## Documentation

- **Dev Containers Docs:** https://code.visualstudio.com/docs/devcontainers/containers
- **Docker Compose:** https://docs.docker.com/compose/
- **uv Package Manager:** https://docs.astral.sh/uv/
- **Rocker Project:** https://rocker-project.org/
- **renv Documentation:** https://rstudio.github.io/renv/
- **pak (R package installer):** https://pak.r-lib.org/
- **Quarto:** https://quarto.org/docs/
