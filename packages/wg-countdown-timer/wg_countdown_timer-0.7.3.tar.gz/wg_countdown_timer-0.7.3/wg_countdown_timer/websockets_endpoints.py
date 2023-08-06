from asyncio import Event
from websockets.exceptions import ConnectionClosed
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketDisconnect
from . countdown import CountdownTimer

class ChangeEndpoint(WebSocketEndpoint):
    encoding = 'text'
    subscribed_people: int = 0
    subscribed_people_event: Event = None

    async def on_connect(self, websocket: WebSocket):
        try:
            await websocket.accept()
            ChangeEndpoint.subscribed_people += 1
            if ChangeEndpoint.subscribed_people_event:
                ChangeEndpoint.subscribed_people_event.set()
                ChangeEndpoint.subscribed_people_event.clear()

            if not CountdownTimer.timer_changed_event:
                CountdownTimer.timer_changed_event = Event()

            await websocket.send_text(CountdownTimer.countdown_data_json)
            while await CountdownTimer.wait_for_changes():
                await websocket.send_text(CountdownTimer.countdown_data_json)
        except (WebSocketDisconnect, ConnectionClosed):
            pass

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        ChangeEndpoint.subscribed_people -= 1
        if ChangeEndpoint.subscribed_people_event:
            ChangeEndpoint.subscribed_people_event.set()
            ChangeEndpoint.subscribed_people_event.clear()

class ChangeSubscribersEndpoint(WebSocketEndpoint):
    encoding = 'text'

    async def on_connect(self, websocket: WebSocket):
        try:
            await websocket.accept()
            if not ChangeEndpoint.subscribed_people_event:
                ChangeEndpoint.subscribed_people_event = Event()

            await websocket.send_text(str(ChangeEndpoint.subscribed_people))
            while await ChangeEndpoint.subscribed_people_event.wait():
                await websocket.send_text(str(ChangeEndpoint.subscribed_people))
        except (WebSocketDisconnect, ConnectionClosed):
            pass