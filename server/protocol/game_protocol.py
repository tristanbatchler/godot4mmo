"""
This module contains the game protocol used for communication between the server and clients.
"""
import logging
from google.protobuf.message import DecodeError
from trio_websocket import WebSocketConnection
import server.net as packets
from server.protocol import states
from server.protocol.logging_adapter import ProtocolLoggerAdapter

class GameProtocol:
    """
    Represents the game protocol used for communication between the server and clients.
    """
    def __init__(self, server_stream: WebSocketConnection, ident: int):
        self._server_connection: WebSocketConnection = server_stream
        self.state = states.EntryState(self)

        # Give this protocol a unique identifier to improve logging
        self.logger = ProtocolLoggerAdapter(logging.getLogger(__name__), {
            'ident': ident,
            'state': self.state
        })

    async def start(self):
        """
        Starts the game protocol and handles incoming messages.

        This method continuously reads messages from the connection and handles them
        until the connection is closed or an exception occurs.

        Raises:
            Exception: If an error occurs while handling a message.
        """
        try:
            while True:
                data = await self._read_message()
                if data is None:
                    break
                await self._handle_message(data)
        finally:
            self.logger.info("Stopped")

    async def send_packet(self, packet: packets.Packet):
        """
        Sends a packet over the network.

        Args:
            packet (packets.Packet): The packet to send.

        Raises:
            Any exceptions that occur during the sending process.
        """
        await self._send_message(packet.SerializeToString())

    def set_state(self, state: states.ProtocolState) -> None:
        """
        Sets the protocol state to the specified state.

        Args:
            state (states.ProtocolState): The state to set.

        Returns:
            None
        """
        if self.state is state:
            self.logger.warning(f"State already set to {state}")
            return

        if state == states.ProtocolState:
            raise ValueError("Cannot set state to ProtocolState")

        self.logger.info(f"State changing to {state}")
        self.state = state
        self.logger.extra['state'] = state

    async def _read_message(self) -> bytes:
        try:
            return await self._server_connection.get_message()

        except Exception as exc:
            self.logger.error(f"Read error: {exc}")
            raise exc

    async def _send_message(self, message: bytes):
        await self._server_connection.send_message(message)

    async def _handle_message(self, data: bytes):
        try:
            packet: packets.Packet = packets.Packet.FromString(data)
        except DecodeError as exc:
            self.logger.warning(f"Failed to decode packet: {exc}")

        # Dispatch to protocol state handler
        packet_type: str = packet.WhichOneof("subpacket")
        handler_name: str = f"handle_{packet_type}_packet"
        try:
            handler: callable = getattr(self.state, handler_name)
            await handler(getattr(packet, packet_type))
        except AttributeError:
            self.logger.error(f"Current state does not support handling of {packet_type} packets")
