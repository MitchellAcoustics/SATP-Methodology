# Managing R Packages with renv

This project uses **renv** for reproducible R package management. R packages are defined in `renv.lock` (not in devcontainer.json).

## Quick Start

### Add a Package

1. Open an R console in the container:
   ```bash
   R
   ```

2. Install the package:
   ```r
   renv::install("package_name")
   ```

3. This automatically updates `renv.lock` with the exact version.

4. Exit R:
   ```r
   q()
   ```

### Restore All Packages (on rebuild)

When the dev container starts, it automatically runs:
```bash
Rscript -e 'renv::restore(prompt=FALSE)'
```

This installs all packages from `renv.lock` using **pak** for fast, parallel installation.

## How It Works

- **renv.lock**: Defines exact versions of all R packages (like `requirements.txt` for Python)
- **pak**: Fast parallel package installer that renv uses when `RENV_CONFIG_PAK_ENABLED=TRUE`
- **Caching**: Downloaded packages cached in `renv-cache` volume for faster rebuilds
- **Reproducibility**: Everyone gets the exact same package versions from `renv.lock`

## Managing Packages

### Add a Package (Interactive)

```bash
# In container terminal
R
> renv::install("tidyverse")
> q()
```

This updates `renv.lock` automatically.

### Add Multiple Packages at Once

```bash
# In container terminal
R
> renv::install(c("ggplot2", "dplyr", "tidyr"))
> q()
```

### Update a Specific Package

```bash
R
> renv::install("package_name")  # Re-installs or upgrades
> q()
```

### View Installed Packages

```bash
R
> renv::status()  # Shows locked vs installed versions
> q()
```

### Snapshot Changes (Advanced)

If you modify `renv.lock` manually:
```bash
R
> renv::snapshot()  # Updates lock file with current library state
> q()
```

## Performance

With pak enabled, package installation is:
- **Parallel**: Multiple packages download/compile simultaneously
- **Cached**: Downloaded binaries stored in `renv-cache` volume
- **Fast**: Binary packages preferred when available (usually on recent R)

First build takes longer (packages compile from source if needed), but subsequent builds are much faster due to caching.

## renv.lock Format

The file contains metadata like:

```json
{
  "R": {
    "Version": "4.2.2",
    "Repositories": [
      {
        "Name": "CRAN",
        "URL": "https://cloud.r-project.org"
      }
    ]
  },
  "Packages": {
    "yaml": {
      "Package": "yaml",
      "Version": "2.3.7",
      "Source": "Repository",
      "Repository": "CRAN",
      "Requirements": [],
      "Hash": "abc123..."
    }
  }
}
```

**Don't edit this manually**—renv updates it automatically when you install packages.

## Troubleshooting

### Package won't install

- Check internet connection
- Try manual install: `Rscript -e 'renv::install("package_name")'`
- Check for system library requirements (e.g., `libfontconfig1-dev` for font-related packages)

### Packages stuck installing

- pak is running packages in parallel—this is normal
- Check available memory; large packages need space to compile
- Monitor with `docker stats satp-dev` in another terminal

### Need to clear cache

```bash
# From host machine
docker volume rm renv-cache
# Then rebuild container
```

### Restore from scratch

```bash
R
> renv::restore(clean = TRUE, prompt = FALSE)  # Remove unlisted packages first
> q()
```

## Recommended Packages

Start with these lightweight packages:
- `yaml` - YAML parsing
- `jsonlite` - JSON handling
- `stringr` - String manipulation

Heavier packages (compile slower but worth it):
- `tidyverse` - Data manipulation
- `ggplot2` - Plotting
- `rmarkdown` - Document generation
