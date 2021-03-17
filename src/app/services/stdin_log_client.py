import sys
from typing import Generator
from app.services.socket import Client


class StdInLogClient(Client):
    def _get_messages(self) -> Generator[str, None, None]:
        for line in sys.stdin:
            yield line
