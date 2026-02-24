#!/bin/bash
# Parse R packages from devcontainer.json and install them
# This script is called during container initialization

set -e

# Extract R packages array from devcontainer.json
R_PACKAGES=$(jq -r '.customizations.vscode.settings."r.packages"? // empty | .[]?' /workspace/.devcontainer/devcontainer.json 2>/dev/null || echo "")

if [ -z "$R_PACKAGES" ]; then
  echo "No R packages specified in devcontainer.json. Skipping R package installation."
  exit 0
fi

# Convert to space-separated string
PACKAGES=$(echo "$R_PACKAGES" | tr '\n' ' ')

echo "Installing R packages: $PACKAGES"

# Call the R installation script (no sudo needed with proper directory permissions)
Rscript /workspace/.devcontainer/install-r-packages.R $PACKAGES

echo "R packages installed successfully."
