import logging
import server.net as packets
import server.protocol.states as states
from trio_websocket import WebSocketConnection
from server.protocol.logging_adapter import ProtocolLoggerAdapter

class GameProtocol:
    def __init__(self, server_stream: WebSocketConnection, ident: int):
        self._server_connection: WebSocketConnection = server_stream
        self.state = states.EntryState(self)

        # Give this protocol a unique identifier to improve logging
        self.logger = ProtocolLoggerAdapter(logging.getLogger(__name__), {
            'ident': ident,
            'state': self.state
        })
        
    async def start(self):
        try:
            while True:
                data = await self._read_message()
                if data is None:
                    break
                await self._handle_message(data)
        except Exception as exc:
            self.logger.error(f"Crashed: {exc!r}")
        finally:
            self.logger.info("Stopped")

    async def send_packet(self, packet: packets.Packet):
        await self._send_message(packet.SerializeToString())

    def set_state(self, state: states.ProtocolState):
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
            
        except Exception as exc:
            self.logger.warning(f"Packet does not exist: {exc}")
        
        # Dispatch to protocol state handler 
        packet_type: str = packet.WhichOneof("subpacket")
        handler_name: str = f"handle_{packet_type}_packet"
        try:
            handler: callable = self.state.__getattribute__(handler_name)
            await handler(packet.__getattribute__(packet_type))
        except AttributeError:
            self.logger.error(f"Current state does not support handling of {packet_type} packets")
        except Exception as exc:
            self.logger.error(f"Packet handling error: {exc!r}")
