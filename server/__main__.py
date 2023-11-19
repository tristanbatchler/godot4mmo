import trio
from trio_websocket import serve_websocket, ConnectionClosed, WebSocketConnection, WebSocketRequest
import logging
import server.net as packets
from server.protocol import GameProtocol

async def handle_connection(request: WebSocketRequest):
    logging.info("New connection")
    connection: WebSocketConnection = await request.accept()
    proto: GameProtocol = GameProtocol(connection)
    await proto.start()


async def main():
    await serve_websocket(handle_connection, 'localhost', 8081, ssl_context=None)

logging.basicConfig(level=logging.INFO)
logging.info(f"Server starting")
trio.run(main)