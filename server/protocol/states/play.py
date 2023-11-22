"""
Play state for the protocol. This state is used for handling packets that are sent/received after 
the player has entered the game world.
"""
from server.net import Packet
from server.protocol.states.protocol_state import ProtocolState

class PlayState(ProtocolState):
    """
    Represents the play state of the protocol. This state is used for handling packets that are 
    sent/received after the player has entered the game world.
    """
    def handle_login_packet(self, packet: Packet):
        self.proto.logger.info(f"Received login packet: {packet}")

    def handle_register_packet(self, packet: Packet):
        self.proto.logger.info(f"Received register packet: {packet}")

    def handle_chat_packet(self, packet: Packet):
        self.proto.logger.info(f"Received chat packet: {packet}")
