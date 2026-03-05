#!/usr/bin/python3
"""
fireplace.py: Python implementation of the Sit Group's Proflame 2 remote fireplace controller.

Uses the correct ECC algorithm (16-mask parity) from rtl_433 issue #1905.
The original johnellinwood/smartfire ECC was incorrect and caused receivers to reject commands.
"""

__version__ = "0.0.2"

import logging
import sys
import time

from rflib import RfCat, MOD_ASK_OOK
from bitstring import Bits, BitArray

# Default serial: 3 bytes (serial_hi, serial_lo, version) - use lower 8 bits of each 9-bit word
# rtl_433 Id format: 21dd02 = 0x21 0xDD 0x02
DEFAULT_SERIAL = ["001001011", "011110100", "000000100"]

# 16-mask parity table for correct ECC (from rtl_433 issue #1905, kaechele's C code)
# Each mask selects bits from the 40-bit data (bytes 0-4) for parity calculation
PF2_MASKS = (
    0x800000C000,
    0x1080006200,
    0x7000003100,
    0xC080001000,
    0x2000008000,
    0xC080004000,
    0x9000002200,
    0x6000001100,
    0x90800000C4,
    0x0000000062,
    0xD000000031,
    0x1000000010,
    0x2000000088,
    0x2080000044,
    0x9080000022,
    0xE000000011,
)


def _parity8(byte_val: int) -> int:
    """Parity of one byte (returns 0 for even, 1 for odd). rtl_433 parity8 helper."""
    byte_val ^= byte_val >> 4
    byte_val &= 0xF
    return (0x6996 >> byte_val) & 1


def _parity64(v: int) -> int:
    """Fold 64-bit value to single parity bit."""
    v ^= v >> 32
    v ^= v >> 16
    v ^= v >> 8
    return _parity8(v & 0xFF)


def _calc_ecc(data: bytes, xor_correction: int = 0) -> int:
    """Calculate 16-bit ECC for bytes 0-4 using correct 16-mask parity algorithm.

    Some remotes (per rtl_433 issue #1905) require xor_correction (e.g. 0x0902).
    """
    if len(data) < 5:
        raise ValueError("Need at least 5 bytes for ECC")
    # Build 40-bit value: d[0] d[1] d[2] d[3] d[4] (MSB first in 64-bit)
    value = (
        (data[0] << 32)
        | (data[1] << 24)
        | (data[2] << 16)
        | (data[3] << 8)
        | data[4]
    )
    ecc = 0
    for mask in PF2_MASKS:
        ecc = (ecc << 1) | _parity64(value & mask)
    return (ecc ^ xor_correction) & 0xFFFF


class Fireplace:
    """Model for the fireplace state and controls."""

    def __init__(self, serial=None, ecc_xor=0):
        self._radio = None
        self._serial = DEFAULT_SERIAL if serial is None else serial
        self._ecc_xor = ecc_xor
        self._pilot = True
        self._light = 0
        self._thermostat = False
        self._power = False
        self._front = False
        self._fan = 0
        self._aux = False
        self._flame = 0

    @property
    def radio(self):
        if self._radio is None:
            self._radio = RfCat()
            self._radio.setFreq(314973000)
            self._radio.setMdmModulation(MOD_ASK_OOK)
            self._radio.setMdmDRate(2400)
        return self._radio

    @property
    def serial(self):
        return self._serial

    @property
    def pilot(self):
        return self._pilot

    @pilot.setter
    def pilot(self, value):
        self.set(pilot=value)

    @property
    def light(self):
        return self._light

    @light.setter
    def light(self, value):
        self.set(light=value)

    @property
    def thermostat(self):
        return self._thermostat

    @thermostat.setter
    def thermostat(self, value):
        self.set(thermostat=value)

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self.set(power=value)

    @property
    def front(self):
        return self._front

    @front.setter
    def front(self, value):
        self.set(front=value)

    @property
    def fan(self):
        return self._fan

    @fan.setter
    def fan(self, value):
        self.set(fan=value)

    @property
    def aux(self):
        return self._aux

    @aux.setter
    def aux(self, value):
        self.set(aux=value)

    @property
    def flame(self):
        return self._flame

    @flame.setter
    def flame(self, value):
        self.set(flame=value)

    @property
    def state(self):
        return {
            "serial": self.serial,
            "pilot": self.pilot,
            "light": self.light,
            "thermostat": self.thermostat,
            "power": self.power,
            "front": self.front,
            "fan": self.fan,
            "aux": self.aux,
            "flame": self.flame,
        }

    @state.setter
    def state(self, values):
        self.set(**values)

    def set(
        self,
        serial=None,
        pilot=None,
        light=None,
        thermostat=None,
        power=None,
        front=None,
        fan=None,
        aux=None,
        flame=None,
    ):
        logging.debug(
            "Setting pilot:%s, light:%s, thermostat:%s, power:%s, front:%s, fan:%s, aux:%s, flame:%s",
            pilot,
            light,
            thermostat,
            power,
            front,
            fan,
            aux,
            flame,
        )
        if pilot is not None:
            self._pilot = pilot
        if light is not None:
            if (light < 0) or (light > 6):
                raise ValueError("Light value must be between 0 and 6 inclusive")
            self._light = light
        if thermostat is not None:
            self._thermostat = thermostat
        if power is not None:
            self._power = power
        if front is not None:
            self._front = front
        if fan is not None:
            if (fan < 0) or (fan > 6):
                raise ValueError("Fan value must be between 0 and 6 inclusive")
            self._fan = fan
        if aux is not None:
            self._aux = aux
        if flame is not None:
            if (flame < 0) or (flame > 6):
                raise ValueError("Flame value must be between 0 and 6 inclusive")
            self._flame = flame

        packet = self.build_packet()
        self.send_packet(packet)

    def _serial_to_bytes(self) -> tuple[int, int, int]:
        """Convert serial (3 words of 9 bits) to serial_hi, serial_lo, version bytes."""
        # Use lower 8 bits of each 9-bit word
        b0 = int(self._serial[0], 2) & 0xFF
        b1 = int(self._serial[1], 2) & 0xFF
        b2 = int(self._serial[2], 2) & 0xFF
        return (b0, b1, b2)

    def build_packet(self) -> BitArray:
        """Build packet using correct 7-byte format and 16-mask ECC.

        Packet format (rtl_433): [serial_hi, serial_lo, version, cmd1, cmd2, err1, err2]
        """
        serial_hi, serial_lo, version = self._serial_to_bytes()

        # CMD1: pilot(1) | light(3) | thermostat(2) | power(1) - rtl_433 bit layout
        thermo_val = 1 if self._thermostat else 0
        cmd1 = (
            ((1 if self._pilot else 0) << 7)
            | ((self._light & 7) << 4)
            | ((thermo_val & 3) << 1)
            | (1 if self._power else 0)
        )

        # CMD2: front/split_flow(1) | fan(3) | aux(1) | flame(3)
        cmd2 = (
            ((1 if self._front else 0) << 7)
            | ((self._fan & 7) << 4)
            | ((1 if self._aux else 0) << 3)
            | (self._flame & 7)
        )

        # Build 5-byte data for ECC
        data = bytes([serial_hi, serial_lo, version, cmd1, cmd2])
        ecc = _calc_ecc(data, self._ecc_xor)
        err1 = (ecc >> 8) & 0xFF
        err2 = ecc & 0xFF

        # 7-byte packet
        pkt = bytes([serial_hi, serial_lo, version, cmd1, cmd2, err1, err2])

        # Manchester encode: Proflame 2 uses word-based encoding
        # Each byte becomes 9-bit word: 0 + 8 bits (leading 0 for word alignment)
        # Format per word: S + 1 + 9 bits + parity + 1 + Z*9
        packet_string = ""
        for byte_val in pkt:
            # 9-bit word: leading 0 + 8 bits of byte
            word_bits = "0" + format(byte_val, "08b")
            packet_string += "S"
            packet_string += "1"
            packet_string += word_bits
            parity = sum(1 for c in word_bits if c == "1") % 2
            packet_string += str(parity)
            packet_string += "1"
            packet_string += "Z" * 9

        manchester_codes = {"S": "11", "0": "01", "1": "10", "Z": "00"}
        packet_array = [manchester_codes[b] for b in packet_string]
        packet = BitArray()
        for b in packet_array:
            packet.append(Bits(bin=b))

        return packet

    def send_packet(self, packet: BitArray) -> None:
        """Transmit the packet over the radio 5 times with proper gaps.

        Proflame 2 protocol requires 5 repetitions separated by 12 zero bits (~5ms at 2400 baud).
        rfcat's repeat parameter is ignored by firmware, so we loop manually.
        """
        # Pad to multiple of 8 for bytes
        pad_bits = (8 - len(packet) % 8) % 8
        if pad_bits:
            packet = packet + Bits(uint=0, length=pad_bits)
        data = bytes(packet.bytes)
        logging.info("Transmitting %s (%d bytes) x5", packet.hex, len(data))
        self.radio.setModeIDLE()
        gap_seconds = 12 / 2400.0
        for i in range(5):
            self.radio.RFxmit(data=data)
            if i < 4:
                time.sleep(gap_seconds)


if __name__ == "__main__":
    fire = Fireplace()
    cmd = "fire.set(" + ",".join(sys.argv[1:]) + ")"
    print(cmd)
    exec(cmd)  # noqa: S102
