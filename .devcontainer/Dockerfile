# Build stage for Python dependencies
FROM python:3.12.5-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_COMPILE_BYTECODE=1

# Install build dependencies and system libraries for rpy2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    r-base \
    r-base-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY pyproject.toml uv.lock* ./

# Install uv and compile dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system --compile-bytecode /build

# Dev container stage
FROM python:3.12.5-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    RENV_PATHS_CACHE=/home/vscode/.cache/R/renv \
    RENV_CONFIG_PAK_ENABLED=TRUE

# Install runtime dependencies, dev tools, and R
# Includes system libraries for R packages with C/C++ dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    r-base \
    r-base-dev \
    libgit2-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    pandoc \
    ca-certificates \
    git \
    curl \
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
    && rm -rf /var/lib/apt/lists/*

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

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files with correct ownership (from root context)
COPY --chown=vscode:vscode . .

# Install uv in the final image for development
RUN pip install --no-cache-dir uv

# Switch to vscode user
USER vscode

# Default command for devcontainer
CMD ["/bin/bash"]
