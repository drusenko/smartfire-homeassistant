# Smartfire Home Assistant Integration

Home Assistant integration for controlling Proflame 2 fireplaces via the YardStick One RF transmitter. Supports both local (YardStick on HA server) and remote (REST server elsewhere) installations.

## Quick Start

### Local Installation (YardStick on Home Assistant server)

1. **Add this repo to HACS** (Integrations) and install the Smartfire integration
2. **Add this repo to the Add-on store** (Settings → Add-ons → Add-on store → Repositories → `https://github.com/davidrusenko/smartfire-homeassistant`)
3. **Install and start** the Smartfire Server add-on
4. **Add the integration** (Settings → Devices & Services → Add Integration → Smartfire)
5. Choose **Local** - you'll get a fireplace switch to turn on/off

> **Note:** If local mode cannot connect, try **Remote** mode instead and enter your Home Assistant server's IP address with port 5000 (e.g., `192.168.1.100:5000`).

### Remote Installation

1. Run the [smartfire](https://github.com/johnellinwood/smartfire) REST server on a Raspberry Pi with YardStick
2. Add this repo to HACS and install the Smartfire integration
3. Add the integration and choose **Remote**
4. Enter your Pi's IP and port (default 5000)

## Hardware

- **YardStick One** - USB RF transceiver (TI CC1101 chipset)
- Compatible with Proflame 2 fireplaces from Jotul, Mendota, Regency, Empire, Lennox, and others

## Repository Structure

- `custom_components/smartfire/` - Home Assistant integration
- `smartfire_server/` - Add-on for running the REST server locally
- `repository.yaml` - Add-on repository configuration

## License

GPL-3.0 (inherited from smartfire project)
