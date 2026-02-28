# Smartfire Home Assistant Integration

Home Assistant integration for controlling Proflame 2 fireplaces via the YardStick One RF transmitter. Supports both local (YardStick on HA server) and remote (REST server elsewhere) installations.

## Quick Start

### Local Installation (YardStick on Home Assistant server)

1. **Add this repo to HACS** (Integrations) and install the Smartfire integration
2. **Add this repo to the Add-on store** (Settings → Add-ons → Add-on store → Repositories → `https://github.com/drusenko/smartfire-homeassistant`)
3. **Install and start** the Smartfire Server add-on (it has USB access for the YardStick - no extra config needed)
4. **Connect the YardStick One** USB dongle to your Home Assistant server
5. **Add the integration** (Settings → Devices & Services → Add Integration → Smartfire)
6. Choose **Local** - you'll get a fireplace switch to turn on/off

### Remote Installation

1. Run the [smartfire](https://github.com/johnellinwood/smartfire) REST server on a Raspberry Pi with YardStick
2. Add this repo to HACS and install the Smartfire integration
3. Add the integration and choose **Remote**
4. Enter your Pi's IP and port (default 5000)

## Hardware

- **YardStick One** - USB RF transceiver (TI CC1101 chipset)
- Compatible with Proflame 2 fireplaces from Jotul, Mendota, Regency, Empire, Lennox, and others

## Why an Add-on?

The Smartfire Server runs as an add-on (not inside the integration) so it can use `usb: true` and get USB access to the YardStick without any manual configuration. Add-ons run in their own container with the right permissions.

## Repository Structure

- `custom_components/smartfire/` - Home Assistant integration (UI, config flow, switch entity)
- `smartfire_server/` - Add-on that runs the REST server with USB access for the YardStick

## License

GPL-3.0 (inherited from smartfire project)
