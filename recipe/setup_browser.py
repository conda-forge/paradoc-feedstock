"""Provision a Chrome/Chromium browser for python-kaleido on the Windows test leg.

paradoc's plot tests render Plotly figures via python-kaleido, which drives a
headless browser through choreographer. No browser ships with conda, and
choreographer's auto-discovery prefers the registry-installed Chrome on the CI
runner -- which stalls the devtools handshake and hangs the suite. The only
reliable override is the BROWSER_PATH env var, so this script resolves a usable
browser and prints its executable path for the caller to assign to BROWSER_PATH.

  Option A: download Chrome-for-Testing (get_chrome_sync returns its exe path).
  Option B: fall back to the runner's pre-installed Edge/Chrome.
"""

import os
import sys

exe = None

# Option A: Chrome-for-Testing, purpose-built for headless automation.
try:
    import kaleido

    exe = str(kaleido.get_chrome_sync())
    if not os.path.exists(exe):
        exe = None
except Exception as err:  # noqa: BLE001 - best effort, fall back below
    sys.stderr.write(f"Chrome-for-Testing download failed, falling back: {err}\n")
    exe = None

# Option B: a browser pre-installed on the CI runner.
if not exe:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            exe = candidate
            break

if not exe:
    sys.stderr.write("No usable browser found for kaleido rendering.\n")
    sys.exit(1)

sys.stderr.write(f"Using browser for kaleido: {exe}\n")
print(exe)
