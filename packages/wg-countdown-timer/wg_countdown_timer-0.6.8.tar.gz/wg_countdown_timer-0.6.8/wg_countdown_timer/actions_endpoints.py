from starlette.responses import PlainTextResponse
from starlette.requests import Request as StarletteRequest
from . countdown import CountdownTimer

class CountdownTimerActionEndpoints():
    @staticmethod
    async def start(request: StarletteRequest) -> PlainTextResponse:
        return PlainTextResponse(CountdownTimer.start())

    @staticmethod
    async def stop(request: StarletteRequest) -> PlainTextResponse:
        return PlainTextResponse(CountdownTimer.stop())

    @staticmethod
    async def reset(request: StarletteRequest) -> PlainTextResponse:
        return PlainTextResponse(CountdownTimer.reset())

    @staticmethod
    async def pause(request: StarletteRequest) -> PlainTextResponse:
        return PlainTextResponse(CountdownTimer.pause())

    @staticmethod
    async def resume(request: StarletteRequest) -> PlainTextResponse:
        return PlainTextResponse(CountdownTimer.resume())