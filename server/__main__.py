"""
This is the main entrypoint for the server. It creates a trio server that listens for websocket 
connections. Each connection is handled by a GameProtocol instance.
"""
import logging
import trio
from trio_websocket import serve_websocket, WebSocketConnection, WebSocketRequest  # type: ignore
from server.protocol import GameProtocol
from server.database import SessionMaker
from server.database.engine import init_engine, get_session_factory

class GameServer:
    """
    Represents a websocket server that handles new connections for the game.
    """
    def __init__(self, tick_rate: float) -> None:
        self._db_session_factory: SessionMaker = get_session_factory(init_engine())
        self._connected_protocols: list[GameProtocol] = []
        self._tick_rate: float = tick_rate
        self._num_connections = 0

    async def handle_connection(self, request: WebSocketRequest):
        """
        Handles a new websocket connection. This function is called by the trio server whenever a 
        new connection is made. This function creates a new GameProtocol instance for the connection 
        and starts it.
        """
        self._num_connections += 1
        logging.info("New connection")
        connection: WebSocketConnection = await request.accept()
        proto: GameProtocol = GameProtocol(connection, self._connected_protocols,
                                           self._num_connections, self._db_session_factory)
        self._connected_protocols.append(proto)
        await proto.start()

    async def tick(self) -> None:
        """
        Tells each connected protocol to tick.
        """
        for protocol in self._connected_protocols:
            await protocol.tick()

    async def run(self) -> None:
        """
        Runs the game server. This function starts the tick loop.
        """
        while True:
            start_time: float = trio.current_time()
            await self.tick()
            elapsed: float = trio.current_time() - start_time
            diff: float = self._tick_rate - elapsed
            if diff > 0:
                await trio.sleep(diff)
            elif diff < 0:
                logging.warning("Tick time budget exceeded by %s seconds", -diff)


async def main() -> None:
    """
    Serves the websocket server and handles new connections.
    """
    server: GameServer = GameServer(1/20)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(serve_websocket, server.handle_connection, 'localhost', 8081, None)
        nursery.start_soon(server.run)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Server starting")
    trio.run(main)
