# Following pixi devcontainer docs: https://pixi.prefix.dev/v0.65.0/integration/editor/vscode/#direnv-extension

FROM mcr.microsoft.com/devcontainers/base:jammy

# Build arguments
ARG R_VERSION=4.2.2
ARG PIXI_VERSION=v0.65.0

# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1 \
#     # RENV_PATHS_CACHE=/home/vscode/.cache/R/renv \
#     RENV_CONFIG_PAK_ENABLED=TRUE \
#     UV_LINK_MODE=copy \
ENV LD_LIBRARY_PATH=/usr/local/lib/R/lib:$LD_LIBRARY_PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    direnv \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L -o /usr/local/bin/pixi -fsSL --compressed "https://github.com/prefix-dev/pixi/releases/download/${PIXI_VERSION}/pixi-$(uname -m)-unknown-linux-musl" \
    && chmod +x /usr/local/bin/pixi \
    && pixi info

# Install quarto
COPY .devcontainer/install_quarto.sh /tmp/install_quarto.sh
RUN chmod +x /tmp/install_quarto.sh && /tmp/install_quarto.sh && rm /tmp/install_quarto.sh

# set some user and workdir settings to work nicely with vscode
USER vscode
WORKDIR /home/vscode

# Copy project files with correct ownership
# COPY --chown=vscode:vscode . .

RUN echo 'eval "$(pixi completion -s bash)"' >> /home/vscode/.bashrc
