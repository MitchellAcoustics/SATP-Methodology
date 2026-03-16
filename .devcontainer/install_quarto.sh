if [ "$(uname -m)" = "aarch64" ]; then
  QUARTO_ARCH="arm64"
else
  QUARTO_ARCH="amd64"
fi

sudo mkdir -p /opt/quarto/${QUARTO_VERSION}

sudo curl -o quarto.tar.gz -L \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${QUARTO_ARCH}.tar.gz"

sudo tar -zxvf quarto.tar.gz \
    -C "/opt/quarto/${QUARTO_VERSION}" \
    --strip-components=1

sudo rm quarto.tar.gz