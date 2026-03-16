#!/bin/bash
set -e

# Install required font tools and font packages
apt-get update && \
    apt-get install -y --no-install-recommends \
        unzip \
        fontconfig \
        fonts-libertinus \
        fonts-font-awesome && \
    rm -rf /var/lib/apt/lists/*

# Update font cache
fc-cache -f -v
