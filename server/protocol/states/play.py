from server.net import Packet
from server.protocol.states.protocol_state import ProtocolState

class PlayState(ProtocolState):
    async def handle_login_packet(self, packet: Packet):
        self.proto.logger.info(f"Received login packet: {packet}")

    async def handle_register_packet(self, packet: Packet):
        self.proto.logger.info(f"Received register packet: {packet}")

    async def handle_chat_packet(self, packet: Packet):
        self.proto.logger.info(f"Received chat packet: {packet}")