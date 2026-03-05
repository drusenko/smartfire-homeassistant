# Smartfire Server

REST API server for Proflame 2 fireplace control. Requires a YardStick One USB RF transmitter connected to the Home Assistant server.

## Configuration

- **Serial** (optional): Your remote's ID for pairing. Two formats:
  - **Hex** (from rtl_433 capture): `21dd02` or `21,dd,02` (serial_hi, serial_lo, version)
  - **Binary**: `001001011,011110100,000000100` (3 words of 9 bits each)
  Leave empty to use the default. To clone your existing remote: capture with `rtl_433 -f 315M -R 207`, note the Id (e.g. `21dd02`), enter it in the config, then pair.
- **ecc_xor** (optional): Some remotes need an ECC correction. If commands beep but don't work, try `0902`. Leave empty for standard.

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
