from asyncio import get_running_loop

from discatpy.core.http import HTTPClient
from discord_typings import GetGatewayBotData

from .gateway import FakeWebsocket, FakeWebsocketMessage


class FakeMixedHttpClient(HTTPClient):
    def __init__(self, token: str, *, api_version: int | None = None) -> None:
        super().__init__(token, api_version=api_version)

    async def ws_connect(self, url: str):  # type: ignore
        ws = FakeWebsocket(get_running_loop())
        await ws._ready.wait()
        await ws.queue.put(
            FakeWebsocketMessage(
                {
                    "op": 10,
                    "d": {"heartbeat_interval": 41250, "session_id": "1234567890"},
                }
            )
        )
        return ws

    async def get_gateway_bot(self) -> GetGatewayBotData:
        return {
            "session_start_limit": {
                "max_concurrency": 1,
                "remaining": 1,
                "reset_after": 0,
                "total": 1,
            },
            "url": "wss://example.com",
            "shards": 1,
        }
