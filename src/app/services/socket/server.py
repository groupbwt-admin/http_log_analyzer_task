import asyncio
import traceback
import logging
from abc import ABC, abstractmethod
from typing import Optional


class Server(ABC):
    def __init__(self, host: str, port: int):
        self._host: str = host
        self._port: int = port
        self._server: Optional[asyncio.base_events.Server] = None
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer_address = writer.get_extra_info("peername")
        try:
            while data := await reader.readuntil():
                message = data.decode()
                self.logger.debug(f"Received {message!r} from {peer_address!r}")
                self._process_message(message)
        except asyncio.IncompleteReadError:
            self.logger.info(f"{peer_address} stream EOF reached")
        writer.close()
        await writer.wait_closed()
        self.logger.info(f"Connection to {peer_address} has been closed")

    @abstractmethod
    def _process_message(self, message: str):
        pass

    async def _start_server(self):
        self._server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        self.logger.info(f"Serving on {self._server.sockets[0].getsockname()}")
        async with self._server:
            await self._server.serve_forever()

    def start(self):
        try:
            asyncio.run(self._start_server())
        except KeyboardInterrupt:
            self.logger.info("SIGTERM received. Exit")
        except Exception as _e:
            self.logger.critical(traceback.format_exc())
