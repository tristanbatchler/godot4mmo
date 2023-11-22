"""
Entry state for the protocol. This state is used for handling packets that are sent/received before 
the player has logged in.
"""
from server.net import Packet, chat
from server.protocol.states.protocol_state import ProtocolState

class EntryState(ProtocolState):
    """
    Represents the entry state of the protocol.

    This state handles packets that are sent/received before the player has logged in.
    """
    def handle_login_packet(self, packet: Packet):
        self.proto.logger.info(f"Received login packet: {packet}")

    def handle_register_packet(self, packet: Packet):
        self.proto.logger.info(f"Received register packet: {packet}")

    def handle_chat_packet(self, packet: Packet):
        self.proto.logger.info(f"Received chat packet: {packet}")
        self.proto.broadcast_packet(chat(packet.msg))
