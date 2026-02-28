# Smartfire - Proflame 2 Fireplace Control

Home Assistant integration for controlling Proflame 2 fireplaces (Jotul, Mendota, Regency, Empire, Lennox, and others) via the RF protocol.

## Features

- **Power control** - Turn your fireplace on and off
- **Local or remote** - Choose between local (YardStick on HA server) or remote (REST server elsewhere)

## Requirements

- **YardStick One** USB RF transceiver (or compatible TI CC1101 device) for local installations
- **Smartfire Server add-on** for local installations (included in this repository)

## Installation

### Via HACS (recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. In HACS, go to **Integrations** → **Add** → search for "Smartfire" or add this repository:
   - Click the three dots menu → **Custom repositories**
   - Add: `https://github.com/davidrusenko/smartfire-homeassistant`
   - Category: Integration
3. Install the Smartfire integration
4. Restart Home Assistant

### For local installations (YardStick on HA server)

1. Add the add-on repository in Home Assistant:
   - **Settings** → **Add-ons** → **Add-on store** → **Repositories**
   - Add: `https://github.com/davidrusenko/smartfire-homeassistant`
2. Install and start the **Smartfire Server** add-on
3. Configure the Smartfire integration (Settings → Devices & Services → Add Integration)
4. Choose **Local** when prompted

### For remote installations

If the Smartfire REST server runs on another device (e.g., a Raspberry Pi):

1. Configure the Smartfire integration
2. Choose **Remote** when prompted
3. Enter the host and port of your Smartfire server

## Configuration

The integration is configured via the UI. No YAML configuration is required.

## Credits

Based on the [smartfire](https://github.com/johnellinwood/smartfire) project by John Ellinwood.
