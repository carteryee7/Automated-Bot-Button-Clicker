#!/usr/bin/env bash
set -euo pipefail

# This script attempts to install system packages (Chromium) and Python dependencies.
# Run as a normal user; the script will use sudo for apt operations.

echo "Updating package lists..."
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  echo "Installing Chromium and common dependencies..."
  sudo apt-get install -y chromium chromium-driver || echo "chromium packages may not be available on this distro; please install Chrome/Chromium manually"
  # Common libraries needed to run headless chrome in minimal containers
  sudo apt-get install -y libxss1 libappindicator3-1 fonts-liberation libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libxcomposite1 libxcursor1 libxdamage1 libxtst6 libnss3 libasound2 libgbm1 || echo "Some optional libs may have failed to install; if chrome fails to start, install the missing libs manually"
else
  echo "apt-get not found. If you're on a different distro, install Chrome/Chromium yourself and ensure it's on PATH."
fi

python3 -m pip install --upgrade pip setuptools
python3 -m pip install -r requirements.txt

echo "Done. You can run the script with: python3 bot.py"
