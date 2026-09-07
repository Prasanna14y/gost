# GhostMe

A cross-platform desktop tool that lets you change your iPhone's GPS location using Apple's developer mode over USB.

## Features

- **USB Connection**: Connect your iPhone via Lightning/USB-C cable
- **Interactive Map**: Pick any location on an interactive world map
- **Search**: Search for locations by name or coordinates
- **Favorites**: Save frequently used locations
- **Reset**: Instantly restore your real GPS location
- **Cross-Platform**: Works on macOS (Apple Silicon & Intel) and Windows

## Requirements

- Python 3.9+
- An iPhone connected via USB
- iTunes/Apple Mobile Device Support installed (Windows)
- On macOS: Xcode command line tools or Apple mobile device framework

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m ghostme
```

Then open your browser to `http://localhost:5000`.

### Steps

1. Connect your iPhone to your computer via USB cable
2. Trust the computer on your iPhone if prompted
3. Launch GhostMe
4. Click on the map or search for a location
5. Click "Set Location" to spoof your GPS
6. Click "Reset Location" to restore real GPS

## How It Works

GhostMe uses Apple's Developer Disk Image (DDI) functionality to set a simulated location on iOS devices. This is the same mechanism Xcode uses for location simulation during app development. The tool communicates with the device over USB using the `pymobiledevice3` library.

## Building Standalone Executables

```bash
pip install pyinstaller
pyinstaller ghostme.spec
```

## License

MIT
