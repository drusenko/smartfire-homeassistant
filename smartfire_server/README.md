# Smartfire Server Add-on

REST server for controlling Proflame 2 fireplaces via the YardStick One RF transmitter.

## Requirements

- **YardStick One** USB RF transceiver (or compatible TI CC1101 device)
- Home Assistant OS or Supervised installation
- The YardStick must be connected via USB to the Home Assistant server

## Installation

1. Add this repository to the Home Assistant add-on store:
   - Go to **Settings** → **Add-ons** → **Add-on store**
   - Click the three dots (⋮) → **Repositories**
   - Add: `https://github.com/davidrusenko/smartfire-homeassistant`
   - Click **Add**

2. Install the **Smartfire Server** add-on
3. Start the add-on
4. Configure the Smartfire integration in Home Assistant (Settings → Devices & Services → Add Integration → Smartfire)
5. Choose "Local" when prompted

## Compatibility

Works with fireplaces using the Sit Group Proflame 2 control system, including:
Jotul, Mendota, Regency, Empire, Lennox, and others.

## Support

For issues, please open a GitHub issue.
