"""
This module contains the game protocol used for communication between the server and clients.
"""
from __future__ import annotations
import logging
from queue import Queue
from typing import Optional
from google.protobuf.message import DecodeError
from trio_websocket import WebSocketConnection, ConnectionClosed
from server.database import SessionMaker
import server.net as packets
from server.protocol import states
from server.protocol.logging_adapter import ProtocolLoggerAdapter

class GameProtocol:
    """
    Represents the game protocol used for communication between the server and clients.
    """
    def __init__(self, server_stream: WebSocketConnection, other_protocols: list[GameProtocol],
                 ident: int, session_factory: SessionMaker) -> None:
        self._server_connection: WebSocketConnection = server_stream
        self._other_protocols: list[GameProtocol] = other_protocols
        self._outgoing_packets: Queue[tuple[GameProtocol, packets.Packet]] = Queue()
        self._ident: int = ident
        self.session_factory = session_factory
        self.state: states.ProtocolState = states.EntryState(self)

        # Give this protocol a unique identifier to improve logging
        self.logger = ProtocolLoggerAdapter(logging.getLogger(__name__), {
            'ident': self._ident,
            'state': self.state
        })

    async def start(self) -> None:
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
                self._handle_message(data)
        finally:
            self.broadcast_packet(
                packets.disconnect(f"Client #{self._ident} has disconnected"), include_self=False)
            self.logger.info("Stopped")
            self._other_protocols.remove(self)

    def set_state(self, state_cls: type[states.ProtocolState]) -> None:
        """
        Sets the protocol state to the specified state.

        Args:
            state_cls (type[states.ProtocolState]): The class of the state to set the protocol to.

        Returns:
            None

        Example:
            >>> protocol.set_state(PlayState)
        """
        if isinstance(self.state, state_cls):
            self.logger.warning(f"State already set to {self.state}")
            return

        if state_cls is states.ProtocolState:
            raise ValueError("Cannot set state to ProtocolState")

        new_state: states.ProtocolState = state_cls(self)
        self.logger.info(f"State changing to {new_state}")
        self.state = new_state
        self.logger.extra['state'] = new_state

    def queue_outbound_packet(self, recipient: GameProtocol, packet: packets.Packet) -> None:
        """
        Queues up a packet to send to another protocol on the next tick.

        Args:
            recipient (GameProtocol): 
                The protocol to send the packet to. If this is the same as this protocol, the packet 
                will be sent directly to the connected client.
            packet (packets.Packet): 
                The packet to send.

        Returns:
            None
        """
        self._outgoing_packets.put((recipient, packet))

    def broadcast_packet(self, packet: packets.Packet, include_self: bool = False) -> None:
        """
        Queues a packet on all connected protocols' outgoing packet queues, optionally including 
        this protocol.

        Args:
            packet (packets.Packet): 
                The packet to broadcast.
            include_self (bool): 
                Whether to include this protocol in the broadcast (in turn, meaning the client
                connected to this protocol will receive the packet directly). Defaults to False.

        Returns:
            None
        """
        for recipient in self._other_protocols:
            if recipient is self and not include_self:
                continue
            recipient.queue_outbound_packet(recipient, packet)

    async def tick(self) -> None:
        """
        Sends the packet at the front of the outgoing packet queue to its destination.
        """
        if self._outgoing_packets.empty():
            return

        recipient, packet = self._outgoing_packets.get()
        if recipient == self:
            await self._send_packet(packet)
        else:
            recipient.queue_outbound_packet(recipient, packet)

    async def _send_packet(self, packet: packets.Packet) -> None:
        self.logger.info(f"Sending packet: {packet}")
        await self._send_message(packet.SerializeToString())

    async def _read_message(self) -> Optional[bytes]:
        try:
            return await self._server_connection.get_message()

        except ConnectionClosed:
            self.logger.info("Connection closed on read")
            return None

        except Exception as exc:
            self.logger.error(f"Read error: {exc}")
            raise exc

    async def _send_message(self, message: bytes) -> None:
        try:
            await self._server_connection.send_message(message)
        except ConnectionClosed:
            self.logger.warning("Connection closed on send")
        except Exception as exc:
            self.logger.error(f"Send error: {exc}")
            raise exc

    def _handle_message(self, data: bytes) -> None:
        try:
            packet: packets.Packet = packets.Packet.FromString(data)
        except DecodeError as exc:
            self.logger.warning(f"Failed to decode packet: {exc}")

        # Dispatch to protocol state handler
        packet_type: str = packet.WhichOneof("type")
        handler_name: str = f"handle_{packet_type}_packet"
        handler: callable = getattr(self.state, handler_name)

        try:
            handler(getattr(packet, packet_type))
        except TypeError:
            self.logger.warning(f"State {self.state} does not implement {handler_name}")
