import inspect
from enum import Enum
from asyncio import AbstractEventLoop

from macrobase.context import context


class HookNames(Enum):
    before_server_start = 0
    # after_server_start = 1    #TODO
    # before_server_stop = 2    #TODO
    after_server_stop = 3


class HookHandler(object):

    def __init__(self, app, handler):
        super().__init__()
        self._app = app
        self._handler = handler

    async def __call__(self, app, loop: AbstractEventLoop):
        if inspect.iscoroutinefunction(self._handler):
            await self._handler(self._app, context, loop)
        else:
            self._handler(self._app, self._app.context, loop)

