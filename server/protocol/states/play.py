"""
Play state for the protocol. This state is used for handling packets that are sent/received after 
the player has entered the game world.
"""
from server.net import ChatPacket, DisconnectPacket, chat, disconnect
from server.protocol.states.protocol_state import ProtocolState
import server.protocol.states as states

class PlayState(ProtocolState):
    """
    Represents the play state of the protocol. This state is used for handling packets that are 
    sent/received after the player has entered the game world.
    """
    def handle_chat_packet(self, packet: ChatPacket):
        self.proto.logger.info(f"Received chat message: {packet.msg}")
        self.proto.broadcast_packet(chat(packet.msg))

    def handle_disconnect_packet(self, packet: DisconnectPacket):
        self.proto.logger.info(f"Received disconnect packet: {packet.reason}")
        self.proto.broadcast_packet(disconnect(packet.reason))
        self.proto.set_state(states.EntryState)
