"""
This module contains all network packet-related logic. Top level functions are used for convenience 
to create packets from the protobuf definitions. E.g. to create a deny packet, use the 
`deny("Not allowed")`, etc. You can of course create the packets manually if you want to, but 
keeping this module up to date with the protobuf definitions is recommended.
"""
# pylint: disable=no-name-in-module
from server.net.packets_pb2 import Packet, OkPacket, DenyPacket, LoginPacket, RegisterPacket, \
    ChatPacket, PositionPacket, DirectionPacket

def _create_packet(packet_type: Packet, **kwargs) -> Packet:
    p: Packet = Packet()
    specific_packet: Packet = packet_type(**kwargs)
    attr_name: str = packet_type.DESCRIPTOR.name.lower().replace("packet", "")
    getattr(p, attr_name).CopyFrom(specific_packet)
    return p

# pylint: disable=missing-function-docstring
def ok() -> Packet:
    return _create_packet(OkPacket)

def deny(reason: str) -> Packet:
    return _create_packet(DenyPacket, reason=reason)

def login(username: str, password: str) -> Packet:
    return _create_packet(LoginPacket, username=username, password=password)

def register(username: str, password: str) -> Packet:
    return _create_packet(RegisterPacket, username=username, password=password)

def chat(message: str) -> Packet:
    return _create_packet(ChatPacket, message=message)

def position(x: float, y: float) -> Packet:
    return _create_packet(PositionPacket, x=x, y=y)

def direction(dx: float, dy: float) -> Packet:
    return _create_packet(DirectionPacket, dx=dx, dy=dy)
