from __future__ import annotations

from abc import ABC, abstractmethod
from server.net import DenyPacket, Packet, create_deny_packet

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from server.protocol import GameProtocol

class ProtocolState(ABC):
    def __init__(self, protocol: GameProtocol):
        self.proto = protocol

    async def log_unregistered_packet(self, packet: Packet):
        self.proto.logger.warning(f"Received {packet.DESCRIPTOR.name} packet in unregistered state")
        p = create_deny_packet("You cannot send that packet in this state")  # todo: better error message
        await self.proto.send_packet(p)
    
    async def handle_login_packet(self, packet: Packet):
        await self.log_unregistered_packet(packet)

    async def handle_register_packet(self, packet: Packet):
        await self.log_unregistered_packet(packet)

    async def handle_chat_packet(self, packet: Packet):
        await self.log_unregistered_packet(packet)