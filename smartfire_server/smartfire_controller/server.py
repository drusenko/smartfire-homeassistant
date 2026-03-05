#!/usr/bin/python3
"""
server.py: REST server providing access to the Proflame 2 controller
Based on https://github.com/johnellinwood/smartfire
"""
import json
import logging
import os

from flask import Flask, request

from fireplace import Fireplace

# Configure logging - use INFO so YardStick status and startup messages are visible
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Suppress Flask's default "Running on http://..." messages (they show container IPs)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

fp = Fireplace()
app = Flask(__name__)


def _check_yardstick(log_result: bool = True) -> bool:
    """Check if YardStick USB device is found. Optionally log result. Return True/False."""
    try:
        _ = fp.radio
        if log_result:
            logger.info("YardStick One USB device found and initialized successfully")
        return True
    except Exception as e:
        if log_result:
            logger.warning("YardStick One USB device NOT found: %s", e)
        return False


def _get_yardstick_status() -> bool:
    """Get YardStick status without logging (for health endpoint)."""
    return _check_yardstick(log_result=False)


@app.route("/state", methods=["GET", "PUT"])
def state():
    """Get or set the whole fireplace state at one time."""
    if request.method == "GET":
        return fp.state
    value = json.loads(request.data)
    fp.set(
        pilot=value.get("pilot"),
        power=value.get("power"),
        flame=value.get("flame"),
    )
    return fp.state


@app.route("/serial", methods=["GET"])
def serial():
    """Return the serial number."""
    return str(fp.serial)


@app.route("/pilot", methods=["GET", "PUT"])
def pilot():
    """Get or set the pilot light."""
    if request.method == "GET":
        return str(fp.pilot)
    fp.pilot = request.data == b"True"
    return str(fp.pilot)


@app.route("/light", methods=["GET", "PUT"])
def light():
    """Get or set the light level."""
    if request.method == "GET":
        return str(fp.light)
    fp.light = int(request.data)
    return str(fp.light)


@app.route("/thermostat", methods=["GET", "PUT"])
def thermostat():
    """Get or set the thermostat."""
    if request.method == "GET":
        return str(fp.thermostat)
    fp.thermostat = request.data == b"True"
    return str(fp.thermostat)


@app.route("/power", methods=["GET", "PUT"])
def power():
    """Get or set the power."""
    if request.method == "GET":
        return str(fp.power)
    fp.power = request.data == b"True"
    return str(fp.power)


@app.route("/front", methods=["GET", "PUT"])
def front():
    """Get or set the front flame."""
    if request.method == "GET":
        return str(fp.front)
    fp.front = request.data == b"True"
    return str(fp.front)


@app.route("/fan", methods=["GET", "PUT"])
def fan():
    """Get or set the fan level."""
    if request.method == "GET":
        return str(fp.fan)
    fp.fan = int(request.data)
    return str(fp.fan)


@app.route("/aux", methods=["GET", "PUT"])
def aux():
    """Get or set the auxiliary power."""
    if request.method == "GET":
        return str(fp.aux)
    fp.aux = request.data == b"True"
    return str(fp.aux)


@app.route("/flame", methods=["GET", "PUT"])
def flame():
    """Get or set the flame level."""
    if request.method == "GET":
        return str(fp.flame)
    fp.flame = int(request.data)
    return str(fp.flame)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for addon monitoring."""
    return {"status": "ok", "yardstick": _get_yardstick_status()}, 200


if __name__ == "__main__":
    # Log YardStick status at startup
    yardstick_ok = _check_yardstick()

    # Log clear startup message - 172.30.x.x is the container's internal Docker IP (normal).
    # The addon's port 5000 is mapped to the host's port 5000.
    # Access from: localhost:5000 (on host) or <home-assistant-ip>:5000 (from LAN)
    logger.info(
        "Smartfire Server starting on 0.0.0.0:5000 - "
        "accessible at localhost:5000 on the host, or <HA-IP>:5000 from your network"
    )
    if not yardstick_ok:
        logger.warning(
            "YardStick not detected - connect the USB dongle and the server will use it when available"
        )

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
