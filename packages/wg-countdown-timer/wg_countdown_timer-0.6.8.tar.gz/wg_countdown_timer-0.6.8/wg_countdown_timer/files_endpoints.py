import os
from starlette.responses import FileResponse
from starlette.requests import Request as StarletteRequest

class CountdownTimerFilesEndpoints():
    @staticmethod
    async def countdown_js(request: StarletteRequest) -> FileResponse:
        return FileResponse(os.path.dirname(os.path.realpath(__file__)) + '/countdown.js', media_type='application/javascript')
