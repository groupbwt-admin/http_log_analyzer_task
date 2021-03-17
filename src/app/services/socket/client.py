import logging
import traceback
import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Generator


class Client(ABC):
    def __init__(self, host: str, port: int):
        self._host: str = host
        self._port: int = port
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    async def _start_client(self):
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        for message in self._get_messages():
            self._write_message(message)

    @abstractmethod
    def _get_messages(self) -> Generator[str, None, None]:
        pass

    def _write_message(self, message: str):
        message = f"{message}\n" if message[-1] != "\n" else message
        if self._writer is not None:
            self._writer.write(message.encode())

    def start(self):
        try:
            asyncio.run(self._start_client())
        except KeyboardInterrupt:
            self.logger.info("SIGTERM received. Exit")
        except Exception as _e:
            self.logger.critical(traceback.format_exc())
