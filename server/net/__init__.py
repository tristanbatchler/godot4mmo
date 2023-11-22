"""
This module contains all network packet-related logic.
"""
# pylint: disable=no-name-in-module
# pylint: disable=missing-function-docstring
from server.net.packets_pb2 import Packet, OkPacket, DenyPacket, LoginPacket, RegisterPacket, \
    ChatPacket, PositionPacket, DirectionPacket

def deny(reason: str) -> Packet:
    p: Packet = Packet()
    d: DenyPacket = DenyPacket(reason=reason)
    p.deny.CopyFrom(d)
    return p
