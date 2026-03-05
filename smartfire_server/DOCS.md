# Smartfire Server

REST API server for Proflame 2 fireplace control. Requires a YardStick One USB RF transmitter connected to the Home Assistant server.

## Configuration

- **Serial** (optional): If your fireplace is paired to a different remote, enter that remote's serial as 3 comma-separated 9-bit binary words. Example: `001001011,011110100,000000100`. Leave empty to use the default (pair the receiver with the YardStick first).

## Pairing

The fireplace receiver must be paired with the YardStick. Press and hold the black Reset button on the receiver until you hear 3 quick beeps, then immediately send a command (e.g. turn on/off from Home Assistant). If pairing succeeds, you'll hear 3 more beeps.

## API Endpoints

- `GET/PUT /power` - Main fireplace power (True/False)
- `GET/PUT /flame` - Flame level (0-6)
- `GET/PUT /fan` - Fan level (0-6)
- `GET/PUT /light` - Light level (0-6)
- `GET/PUT /pilot` - Pilot light (True/False)
- `GET/PUT /front` - Front flame (True/False)
- `GET/PUT /aux` - Auxiliary outlet (True/False)
- `GET/PUT /thermostat` - Thermostat (True/False)
- `GET /health` - Health check
