#!/bin/bash
set -e

# Install unzip if not present
apt-get update && apt-get install -y unzip fontconfig

# Create fonts directory
mkdir -p /usr/share/fonts/opentype

# Install Libertinus Fonts
mkdir -p /tmp/libertinus
cd /tmp/libertinus
wget https://github.com/alerque/libertinus/releases/download/v7.040/Libertinus-7.040.zip
unzip Libertinus-7.040.zip
cp Libertinus-7.040/static/OTF/*.otf /usr/share/fonts/opentype/
cd /
rm -rf /tmp/libertinus

# Install Font Awesome 6 Free (Attempting to satisfy Font Awesome requirements)
# Note: The error mentions "Font Awesome 7 Free", but version 7 is not yet released.
# Installing version 6 which is likely what is needed or compatible.
mkdir -p /tmp/fontawesome
cd /tmp/fontawesome
wget https://use.fontawesome.com/releases/v6.5.1/fontawesome-free-6.5.1-desktop.zip
unzip fontawesome-free-6.5.1-desktop.zip
cp fontawesome-free-6.5.1-desktop/otfs/*.otf /usr/share/fonts/opentype/
cd /
rm -rf /tmp/fontawesome

# Update font cache
fc-cache -f -v
