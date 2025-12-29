# Automated Bot Button Clicker

This repository contains a small Selenium-based script to click a specified button on chess.com (e.g., the cookie consent "Accept" button).

Quick start

1. Install system dependencies and Python packages:

   ```bash
   ./install_deps.sh
   ```

2. Run the script. Examples:

   - Try default behavior (attempts common cookie/consent buttons):
     ```bash
     python3 bot.py
     ```

   - Provide a CSS selector:
     ```bash
     python3 bot.py --selector-type css --selector ".cc-button-component.cc-button-primary"
     ```

   - Run headless:
     ```bash
     python3 bot.py --headless
     ```

Troubleshooting

- If Chrome/Chromium fails to start with "session not created: Chrome instance exited", ensure you have a Chrome/Chromium binary installed that matches the platform and required libraries. On Debian/Ubuntu, the `install_deps.sh` script attempts to install `chromium` and common libraries, but in some environments (e.g., snap-based installations or minimal containers) additional packages may be required.

- If Chrome is installed but still fails to start, try running the script on a non-container machine with a full Chrome installation, or ensure the following libraries are present: `libxss1`, `libatk1.0-0`, `libgtk-3-0`, `libnss3`, `libgbm1`, `libasound2`.

- You can also run the bot on a desktop with Chrome installed and visible (not headless) for debugging.

Notes

- The script uses `webdriver-manager` to install a compatible ChromeDriver automatically.
- Use `--selector-type` and `--selector` to target specific elements (CSS, XPath, or visible button text).
