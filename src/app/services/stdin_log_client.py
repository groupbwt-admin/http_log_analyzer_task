import sys
from typing import Generator
from app.services.socket import Client


class StdInLogClient(Client):
    """
    Log Client class which retrieves messages as lines from stdin
    """
    def _get_messages(self) -> Generator[str, None, None]:
        for line in sys.stdin:
            yield line
