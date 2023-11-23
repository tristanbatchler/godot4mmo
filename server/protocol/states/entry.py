"""
Entry state for the protocol. This state is used for handling packets that are sent/received before 
the player has logged in.
"""
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from server.models import User
from server.net import Packet, RegisterPacket, LoginPacket, ok, deny
from server.protocol.states.protocol_state import ProtocolState
from server.protocol.states.play import PlayState

class EntryState(ProtocolState):
    """
    Represents the entry state of the protocol.

    This state handles packets that are sent/received before the player has logged in.
    """
    def handle_login_packet(self, packet: LoginPacket):
        with self.proto.session_factory() as session:
            try:
                # Check if the username exists
                error_msg: str = "Invalid username or password"
                user: User = session.query(User).filter_by(username=packet.username).first()
                if user is None:
                    deny_packet: Packet = deny(error_msg)
                    self.proto.queue_outbound_packet(self.proto, deny_packet)
                    return

                # Check if the password is correct
                if not bcrypt.checkpw(packet.password.encode(), user.password):
                    deny_packet: Packet = deny(error_msg)
                    self.proto.queue_outbound_packet(self.proto, deny_packet)
                    return

                # Login successful
                ok_packet: Packet = ok("Successfully logged in")
                self.proto.queue_outbound_packet(self.proto, ok_packet)
                self.proto.set_state(PlayState)

            except SQLAlchemyError as exc:
                error_msg: str = "An error occurred while logging in"
                self.proto.logger.error(f"{error_msg}: {exc!r}")
                session.rollback()
                deny_packet: Packet = deny(error_msg)
                self.proto.queue_outbound_packet(self.proto, deny_packet)


    def handle_register_packet(self, packet: RegisterPacket):
        with self.proto.session_factory() as session:
            try:
                # Check if the username is already taken
                if session.query(User).filter_by(username=packet.username).first() is not None:
                    deny_packet: Packet = deny("Username already taken")
                    self.proto.queue_outbound_packet(self.proto, deny_packet)
                    return

                # Create the user
                pw_hash: bytes = bcrypt.hashpw(packet.password.encode(), bcrypt.gensalt())
                user: User = User(username=packet.username, password=pw_hash)
                session.add(user)
                session.commit()
                ok_packet: Packet = ok("Successfully registered")
                self.proto.queue_outbound_packet(self.proto, ok_packet)

            except SQLAlchemyError as exc:
                error_msg: str = "An error occurred while registering"
                self.proto.logger.error(f"{error_msg}: {exc!r}")
                session.rollback()
                deny_packet: Packet = deny(error_msg)
                self.proto.queue_outbound_packet(self.proto, deny_packet)
