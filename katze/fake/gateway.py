import json
from asyncio import AbstractEventLoop, Event, Queue
from typing import Any

from aiohttp import WSMsgType
from disfake import Guild, State, User


class FakeWebsocketMessage:
    def __init__(self, data: Any) -> None:
        self.type = WSMsgType.TEXT
        if isinstance(data, str):
            self.data = data
        else:
            self.data = json.dumps(data)


class FakeWebsocket:
    def __init__(self, loop: AbstractEventLoop):
        self.closed = False
        self.state = State(0, 1)
        self.token: str | None = None
        self._ready = Event()
        loop.create_task(self.__init_task())

    async def __init_task(self):
        self.queue: Queue[FakeWebsocketMessage | str] = Queue()
        self._ready.set()

    async def close(self, *, code: Any):
        self.closed = True

    async def send_json(self, data: Any):
        if data["op"] == 2:
            user = User(self.state)
            guild = Guild(self.state)
            self.token = data["d"]["token"]
            await self.queue.put(
                FakeWebsocketMessage(
                    {"op": 0, "t": "READY", "d": {"v": 9, "user": user.generate()}}
                )
            )
            for _ in range(10):
                await self.queue.put(
                    FakeWebsocketMessage(
                        {
                            "op": 0,
                            "t": "GUILD_CREATE",
                            "d": guild.generate(),
                        }
                    )
                )

    async def receive(self):
        return await self.queue.get()
