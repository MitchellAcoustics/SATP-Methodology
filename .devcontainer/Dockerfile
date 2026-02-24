# Build arguments
ARG R_VERSION=4.2.2

# Dev container stage - use rocker for proper R version support
FROM rocker/r-ver:${R_VERSION}

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    RENV_PATHS_CACHE=/home/rstudio/.cache/R/renv \
    RENV_CONFIG_PAK_ENABLED=TRUE \
    UV_LINK_MODE=copy \
    LD_LIBRARY_PATH=/usr/local/lib/R/lib:$LD_LIBRARY_PATH

# Install Python, R dev libs, and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-venv \
    python3-pip \
    libcurl4-openssl-dev \
    libpcre2-dev \
    libbz2-dev \
    liblzma-dev \
    libicu-dev \
    libssl-dev \
    libxml2-dev \
    ca-certificates \
    git \
    wget \
    sudo \
    build-essential \
    jq \
    pkg-config \
    libfontconfig1-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary from official distroless image
COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /uvx /bin/

# Create vscode user (matching VS Code devcontainer conventions)
RUN groupadd --gid 1000 vscode && \
    useradd -s /bin/bash --uid 1000 --gid 1000 -m vscode && \
    echo "vscode ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/vscode && \
    mkdir -p /home/vscode/.cache && \
    mkdir -p /home/vscode/.cache/R/renv && \
    mkdir -p /home/vscode/.cache/R/pkgcache/pkg && \
    chown -R vscode:vscode /home/vscode

# Configure R library directory for vscode user to write packages
RUN mkdir -p /usr/local/lib/R/site-library && \
    chmod 2777 /usr/local/lib/R/site-library && \
    mkdir -p /usr/lib/R/site-library && \
    chmod 2777 /usr/lib/R/site-library

# Install renv system-wide for bootstrap
RUN Rscript -e "install.packages('renv', repos='https://cloud.r-project.org')"

WORKDIR /workspace

# Copy project files with correct ownership
COPY --chown=vscode:vscode . .

# Switch to vscode user
USER vscode

# Default command for devcontainer
CMD ["/bin/bash"]
