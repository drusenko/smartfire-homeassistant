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

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.environ.get("DEBUG") else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

fp = Fireplace()
app = Flask(__name__)


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
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
