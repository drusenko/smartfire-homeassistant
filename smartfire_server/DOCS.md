# Smartfire Server

REST API server for Proflame 2 fireplace control. Requires a YardStick One USB RF transmitter connected to the Home Assistant server.

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
