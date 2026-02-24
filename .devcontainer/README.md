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
   - The container will automatically run `uv sync` to install Python dependencies
   - Then `renv::restore()` to install all R packages from `renv.lock`
   - R packages install in parallel using pak for speed
   - You're ready to work once the terminal is ready

## What's Inside

The dev container includes:

- **Python 3.12.5** with all project dependencies (rpy2, xarray, circumplex, soundscapy, etc.)
- **R 4.2.2** with development libraries for rpy2 integration
- **renv** for reproducible R package management with pak for fast installation
- **Quarto** for document rendering and publishing
- **Jupyter** support for interactive notebooks
- **Git, uv, and development tools** pre-installed
- **Ruff** for Python linting and formatting
- **VS Code extensions** for Python, Jupyter, Quarto, R, Docker, and Git

## Customizing Python and R Versions

To use different Python or R versions, edit `.devcontainer/devcontainer.json`:

```json
"build": {
    "dockerfile": "Dockerfile",
    "context": ".",
    "args": {
        "PYTHON_VERSION": "3.11.8",
        "R_VERSION": "4.3.1"
    }
}
```

Then rebuild: `Dev Containers: Rebuild Container`

**Available versions:**
- **Python:** Any version available on Docker Hub (e.g., `3.10`, `3.11.8`, `3.12.5`)
- **R:** Any version available from official R repositories (e.g., `4.2.2`, `4.3.1`)

The same versions are also referenced in:
- `.devcontainer/docker-compose.yaml` (for manual builds)

## Environment

- **Working directory:** `/workspace` (mounted to your local project)
- **Python path:** Configured to use `.venv/bin/python`
- **Volumes:**
  - Cache volume for faster builds and package downloads
  - Virtual environment volume for persistence
  - renv cache volume for R package caching
  - pak cache volume for R package binary caching
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

### Python package installation fails

- Run `uv sync` manually: Open terminal in VS Code and run the command
- Check internet connection (some packages pull from GitHub)
- Clear cache if needed: `docker volume prune`

### R package restoration fails

- Check the error in VS Code's terminal during `postCreateCommand`
- Most issues are missing system libraries (Dockerfile has common ones pre-installed)
- Try manual installation: `Rscript -e 'renv::install("package_name")'`
- See [R_PACKAGES.md](./R_PACKAGES.md) for troubleshooting

### R integration issues

- Verify rpy2 loaded: `python -c "import rpy2; print(rpy2.__version__)"`
- Check R path: `which R` (should show `/usr/bin/R`)
- Check renv status: `Rscript -e 'renv::status()'`

### Jupyter kernel connection issues

- Restart VS Code Jupyter kernel: `Shift+Cmd+P` → "Jupyter: Restart Kernel"
- Reload VS Code window: `Cmd+R` (Mac) or `F5` (Windows/Linux)

### Version mismatch after changing Python/R versions

If you change versions in `devcontainer.json`, you need a clean rebuild:
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

- The `.venv` is stored in a named volume for faster I/O on Docker Desktop
- R packages cached in `renv-cache` volume for speedy rebuilds
- Python cache directory persists between builds to speed up package downloads
- renv uses **pak** for parallel package installation (significantly faster than sequential)
- Workspace is mounted with `:cached` for better performance on macOS

## Documentation

- **Dev Containers Docs:** https://code.visualstudio.com/docs/devcontainers/containers
- **Docker Compose:** https://docs.docker.com/compose/
- **uv Package Manager:** https://docs.astral.sh/uv/
- **renv Documentation:** https://rstudio.github.io/renv/
- **pak (R package installer):** https://pak.r-lib.org/
- **Quarto:** https://quarto.org/docs/
