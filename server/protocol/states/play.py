"""
Play state for the protocol. This state is used for handling packets that are sent/received after 
the player has entered the game world.
"""
from server.net import ChatPacket
from server.protocol.states.protocol_state import ProtocolState

class PlayState(ProtocolState):
    """
    Represents the play state of the protocol. This state is used for handling packets that are 
    sent/received after the player has entered the game world.
    """
    def handle_chat_packet(self, packet: ChatPacket):
        self.proto.logger.info(f"Received chat message: {packet.msg}")
        self.proto.broadcast_packet(packet, include_self=False)
