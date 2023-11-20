"""
This module contains the game protocol used for communication between the server and clients.
"""
from __future__ import annotations
import logging
from queue import Queue
from typing import Optional
from google.protobuf.message import DecodeError
from trio_websocket import WebSocketConnection, ConnectionClosed
import server.net as packets
from server.protocol import states
from server.protocol.logging_adapter import ProtocolLoggerAdapter

class GameProtocol:
    """
    Represents the game protocol used for communication between the server and clients.
    """
    def __init__(self, server_stream: WebSocketConnection,
                 other_protocols: list[GameProtocol]) -> None:
        self._server_connection: WebSocketConnection = server_stream
        self._other_protocols: list[GameProtocol] = other_protocols
        self._outgoing_packets: Queue[tuple[GameProtocol, packets.Packet]] = Queue()
        self.state = states.EntryState(self)

        # Give this protocol a unique identifier to improve logging
        self.logger = ProtocolLoggerAdapter(logging.getLogger(__name__), {
            'ident': len(other_protocols),
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
                await self._handle_message(data)
        finally:
            self.logger.info("Stopped")

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

    def queue_outbound_packet(self, other: GameProtocol, packet: packets.Packet) -> None:
        """
        Queues up a packet to send to another protocol on the next tick.

        Args:
            other (GameProtocol): 
                The protocol to send the packet to. If this is the same as this protocol, the packet 
                will be sent directly to the connected client.
            packet (packets.Packet): 
                The packet to send.

        Returns:
            None
        """
        self._outgoing_packets.put((other, packet))

    def broadcast_packet(self, packet: packets.Packet, include_self: bool) -> None:
        """
        Queues a packet on all connected protocols' outgoing packet queues, optionally including 
        this protocol.

        Args:
            packet (packets.Packet): 
                The packet to broadcast.
            include_self (bool): 
                Whether to include this protocol in the broadcast (in turn, meaning the client
                connected to this protocol will receive the packet directly).

        Returns:
            None
        """
        for protocol in self._other_protocols:
            if protocol is self and not include_self:
                continue
            protocol.queue_outbound_packet(protocol, packet)

    async def tick(self) -> None:
        """
        Sends the packet at the front of the outgoing packet queue to its destination.
        """
        if self._outgoing_packets.empty():
            return

        other, packet = self._outgoing_packets.get()
        if other == self:
            await self._send_packet(packet)
        else:
            other.queue_outbound_packet(other, packet)

    async def _send_packet(self, packet: packets.Packet) -> None:
        await self._send_message(packet.SerializeToString())

    async def _read_message(self) -> Optional[bytes]:
        try:
            return await self._server_connection.get_message()

        except ConnectionClosed:
            self.logger.info("Connection closed")
            return None

        except Exception as exc:
            self.logger.error(f"Read error: {exc}")
            raise exc

    async def _send_message(self, message: bytes) -> None:
        await self._server_connection.send_message(message)

    async def _handle_message(self, data: bytes) -> None:
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
