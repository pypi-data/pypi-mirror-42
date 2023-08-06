from starlette.applications import Starlette
from . countdown import CountdownTimer
from . actions_endpoints import CountdownTimerActionEndpoints
from . files_endpoints import CountdownTimerFilesEndpoints
from . websockets_endpoints import ChangeEndpoint, ChangeSubscribersEndpoint

class WGCountdownTimer():
    _server: Starlette

    @classmethod
    def initialize(cls) -> None:
        CountdownTimer.initialize()

        cls._server = Starlette()

        # HTTP Routes for CountdownTimer actions
        cls._server.add_route('/countdown/start', CountdownTimerActionEndpoints.start, methods=['POST'])
        cls._server.add_route('/countdown/reset', CountdownTimerActionEndpoints.reset, methods=['POST'])
        cls._server.add_route('/countdown/stop', CountdownTimerActionEndpoints.stop, methods=['POST'])
        cls._server.add_route('/countdown/pause', CountdownTimerActionEndpoints.pause, methods=['POST'])
        cls._server.add_route('/countdown/resume', CountdownTimerActionEndpoints.resume, methods=['POST'])

        # HTTP Routes for Client-Side JavaScript CountdownTimer script
        cls._server.add_route('/client/countdown.js', CountdownTimerFilesEndpoints.countdown_js, methods=['GET'])

        # WebSockets routes for real-time CountdownTimer data exchange
        cls._server.add_websocket_route('/ws/countdown/change', ChangeEndpoint)
        cls._server.add_websocket_route('/ws/countdown/change/subscribers', ChangeSubscribersEndpoint)
