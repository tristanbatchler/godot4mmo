"""
This is the main entrypoint for the server. It creates a trio server that listens for websocket 
connections. Each connection is handled by a GameProtocol instance.
"""
import dataclasses
import logging
import trio
from trio_websocket import serve_websocket, WebSocketConnection, WebSocketRequest
from server.protocol import GameProtocol

@dataclasses.dataclass
class GameServer:
    """
    Represents a websocket server that handles new connections for the game.
    """
    def __init__(self):
        self._num_connections: int = 0

    async def handle_connection(self, request: WebSocketRequest):
        """
        Handles a new websocket connection. This function is called by the trio server whenever a 
        new connection is made. This function creates a new GameProtocol instance for the connection 
        and starts it.
        """
        logging.info("New connection")
        connection: WebSocketConnection = await request.accept()
        proto: GameProtocol = GameProtocol(connection, self._num_connections)
        self._num_connections += 1
        await proto.start()


async def main():
    """
    Serves the websocket server and handles new connections.
    """
    server: GameServer = GameServer()
    await serve_websocket(server.handle_connection, 'localhost', 8081, ssl_context=None)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Server starting")
    trio.run(main)
