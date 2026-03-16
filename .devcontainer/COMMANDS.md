# Common Dev Container Commands

## VS Code Shortcuts

| Action | Command |
|--------|---------|
| Open in Container | `Cmd+Shift+P` → "Dev Containers: Open in Container" |
| Rebuild Container | `Cmd+Shift+P` → "Dev Containers: Rebuild Container" |
| Remove Container | `Cmd+Shift+P` → "Dev Containers: Remove Container" |
| Reopen Locally | `Cmd+Shift+P` → "Dev Containers: Reopen Folder Locally" |
| Open Terminal | `` Ctrl+` `` (backtick) |

## Inside Container (Terminal)

### Python / uv

```bash
# Install/update dependencies
uv sync

# Add a new package
uv add package_name

# Run a script
uv run computation/script.py

# Enter Python REPL
python

# Check installed packages
uv pip list
```

### Jupyter Notebooks

```bash
# Start Jupyter in background (accessible via VS Code UI)
jupyter notebook --no-browser --ip 0.0.0.0 --port 8888

# Or run cells directly in VS Code
# Open .ipynb file → Run All / Run Cell
```

### Quarto

```bash
# Preview document live
quarto preview index.qmd

# Render to HTML
quarto render index.qmd --to html

# Render to PDF
quarto render index.qmd --to pdf

# Render all formats
quarto render index.qmd
```

### R Integration (via rpy2)

```bash
# Test R connection
python -c "from rpy2 import robjects; robjects.r('print(R.version)')"

# Or in Python script/Jupyter:
from rpy2 import robjects as ro
ro.r('your_r_code_here')
```

### Git

```bash
# Commits persist in container (volume-backed)
git add .
git commit -m "Your message"
git push

# Git history available via GitLens in VS Code
```

### System

```bash
# Check Python version
python --version

# Check R version
R --version

# Check Quarto version
quarto --version

# Check uv version
uv --version

# Current user (should be vscode)
whoami
```

## Troubleshooting Commands

```bash
# Verify all dependencies loaded
python -c "import circumplex, rpy2, xarray, soundscapy; print('✓')"

# Check Python path
which python

# Check R path
which R

# Check virtual environment
echo $VIRTUAL_ENV

# View container logs
docker logs satp-dev-$USER

# Inspect container
docker inspect satp-dev-$USER

# Check disk usage in container
df -h /workspace
```

## Useful Docker Commands (from Host)

```bash
# List running containers
docker ps

# View container logs
docker logs satp-dev-$USER

# Execute command in running container
docker exec satp-dev-$USER uv sync

# Connect to running container bash
docker exec -it satp-dev-$USER bash

# Check container resource usage
docker stats satp-dev-$USER

# Stop container
docker stop satp-dev-$USER

# Start container
docker start satp-dev-$USER

# Remove container and volumes
docker compose -f .devcontainer/docker-compose.yaml down -v
```

## Notes

- **Workspace auto-mounts:** Your local project folder is always synced into `/workspace` in the container
- **Environment persistence:** Files, git history, and package cache persist between sessions
- **No code reload needed:** Edit files locally → they're immediately available in container
- **Terminal always available:** VS Code terminal panel runs commands inside the container automatically
