# GhostMe

A cross-platform desktop tool that lets you change your iPhone's GPS location using Apple's developer mode over USB.

## What is GhostMe?

GhostMe is a program for macOS and Windows that lets you spoof your iPhone's current location. It uses Apple's built-in developer mode feature to simulate GPS coordinates — the same mechanism Xcode uses during app development. No jailbreak required.

## Features

- **USB Connection** — Connect your iPhone via Lightning or USB-C cable
- **Interactive Map** — Click anywhere on a dark-themed world map to pick a location
- **Location Search** — Search for any place by name (powered by OpenStreetMap)
- **Coordinate Entry** — Type exact latitude/longitude values
- **Favorites** — Save and reuse your frequently spoofed locations
- **Reset** — Instantly restore your real GPS with one click
- **Cross-Platform** — Works on macOS (Apple Silicon & Intel) and Windows

## Requirements

| Requirement | Details |
|---|---|
| **Python** | 3.9 or newer |
| **iPhone** | Any iPhone connected via USB |
| **macOS** | Xcode Command Line Tools (`xcode-select --install`) |
| **Windows** | [iTunes](https://www.apple.com/itunes/) or Apple Mobile Device Support installed |

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/Prasanna14y/gost.git
cd gost
```

### Step 2: Create a virtual environment (recommended)

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pymobiledevice3` — Communicates with your iPhone over USB
- `flask` — Runs the local web UI

## How to Use

### 1. Connect your iPhone

Plug your iPhone into your computer using a Lightning or USB-C cable. If this is the first time, tap **Trust** on the "Trust This Computer?" prompt on your iPhone.

### 2. Launch GhostMe

```bash
python -m ghostme
```

This starts a local server and automatically opens your browser to `http://localhost:5000`.

**Command-line options:**

| Flag | Description |
|---|---|
| `--port 8080` | Use a different port (default: 5000) |
| `--no-browser` | Don't auto-open the browser |
| `--debug` | Enable debug logging |

### 3. Set a fake location

You have three ways to pick a location:

- **Click the map** — Click anywhere on the interactive map
- **Search** — Type a place name (e.g., "Tokyo Tower") in the search box and press Enter
- **Coordinates** — Enter exact latitude and longitude values in the input fields

Then click the **Set Location** button. Your iPhone's GPS will immediately update to the new coordinates.

### 4. Reset to real GPS

Click the **Reset** button to restore your iPhone's actual GPS location.

### 5. Save favorites

After selecting a location, click **Save to Favorites** to save it for quick access later. Favorites persist between sessions.

## Building Standalone Executables

You can package GhostMe as a standalone app so it runs without Python installed.

```bash
pip install pyinstaller
pyinstaller ghostme.spec
```

The built executable will be in the `dist/` folder:
- **macOS**: `dist/GhostMe.app`
- **Windows**: `dist/GhostMe.exe`

## Troubleshooting

| Problem | Solution |
|---|---|
| "No device detected" | Make sure your iPhone is unlocked and you've tapped Trust on the popup |
| Device not showing on Windows | Install or reinstall [iTunes](https://www.apple.com/itunes/) to get Apple Mobile Device drivers |
| Device not showing on macOS | Run `xcode-select --install` to install command line tools |
| "Failed to set location" | Your iPhone may need Developer Mode enabled (Settings > Privacy & Security > Developer Mode on iOS 16+) |
| Port 5000 already in use | Run with `--port 8080` or another free port |

## How It Works

GhostMe communicates with your iPhone over USB using the `pymobiledevice3` library. It leverages Apple's Developer Disk Image (DDI) functionality to set a simulated location — this is the exact same API that Xcode uses when you simulate locations during app development. The tool:

1. Detects connected iOS devices via the USB multiplexer (usbmuxd)
2. Establishes a lockdown connection to the device
3. Mounts the Developer Disk Image if needed
4. Sends simulated GPS coordinates through the developer services

No data is sent to any external server. Everything runs locally on your machine.

## License

MIT
