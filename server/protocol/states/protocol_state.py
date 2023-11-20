"""
ProtocolState is an abstract class that represents a state in the protocol. Each state is used for 
handling packets that are sent/received in a specific context. For example, the EntryState is used 
for handling packets that are sent/received before the player has logged in. This way, we can 
separate the logic for handling packets into different states, which makes it easier to manage and 
maintain the code.
"""
from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING
from server.net import DenyPacket, Packet
if TYPE_CHECKING:
    from server.protocol import GameProtocol

class ProtocolState(ABC):
    """
    Abstract protocol state class. This class is used for handling packets that are sent/received in 
    a specific context. Implementations of this class should override the handle_*_packet methods.
    """
    def __init__(self, protocol: GameProtocol):
        self.proto = protocol

    def _log_unregistered_packet(self, packet: Packet):
        self.proto.logger.warning(f"Received {packet.DESCRIPTOR.name} packet in unregistered state")
        p: DenyPacket = DenyPacket()
        p.reason = "You cannot send that packet in this state"
        self.proto.queue_outbound_packet(self.proto, p)

    # Maintain all handle_*_packet methods in alphabetical order. This means classes that inherit
    # from this class will have the deny packet handler by default, unless they specifically
    # override it.

    # pylint: disable=missing-function-docstring
    def handle_chat_packet(self, packet: Packet):
        self._log_unregistered_packet(packet)

    def handle_deny_packet(self, packet: Packet):
        self._log_unregistered_packet(packet)

    def handle_direction_packet(self, packet: Packet):
        self._log_unregistered_packet(packet)

    def handle_login_packet(self, packet: Packet):
        self._log_unregistered_packet(packet)

    def handle_ok_packet(self, packet: Packet):
        self._log_unregistered_packet(packet)

    def handle_position_packet(self, packet: Packet):
        self._log_unregistered_packet(packet)

    def handle_register_packet(self, packet: Packet):
        self._log_unregistered_packet(packet)
    # pylint: enable=missing-function-docstring

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return str(self)
