import trio
from trio_websocket import serve_websocket, ConnectionClosed
import logging
import server.net as packets

async def echo_server(request) -> None:
    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()

            try:
                packet = packets.Packet.FromString(message)
            except Exception as exc:
                logging.error(f"Received invalid packet: {exc!r}")
                return
            
            # Dispatch
            if packet.HasField("ok"):
                logging.info(f"Received OK packet")
            elif packet.HasField("deny"):
                logging.info(f"Received DENY packet: {packet.deny.reason}")
            elif packet.HasField("login"):
                logging.info(f"Received LOGIN packet: {packet.login.username} {packet.login.password}")
            elif packet.HasField("register"):
                logging.info(f"Received REGISTER packet: {packet.register.username} {packet.register.password}")
            elif packet.HasField("chat"):
                logging.info(f"Received CHAT packet: {packet.chat.msg}")
            elif packet.HasField("position"):
                logging.info(f"Received POSITION packet: {packet.position.x} {packet.position.y}")
            elif packet.HasField("direction"):
                logging.info(f"Received DIRECTION packet: {packet.direction.dx} {packet.direction.dy}")
            else:
                raise NotImplementedError(f"Behaviour for packet undefined: {packet!r}")

            # As a test, just echo the packet back to the client
            await ws.send_message(message)

        except ConnectionClosed:
            logging.info('Connection was closed')
            return

async def main():
    await serve_websocket(echo_server, 'localhost', 8081, ssl_context=None)

logging.basicConfig(level=logging.INFO)
logging.info(f"Server starting")
trio.run(main)