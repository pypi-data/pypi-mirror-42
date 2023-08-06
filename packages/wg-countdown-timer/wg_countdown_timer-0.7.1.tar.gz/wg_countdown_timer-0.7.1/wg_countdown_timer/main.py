from starlette.applications import Starlette
from . countdown import CountdownTimer
from . actions_endpoints import CountdownTimerActionEndpoints
from . files_endpoints import CountdownTimerFilesEndpoints
from . websockets_endpoints import ChangeEndpoint, ChangeSubscribersEndpoint

class WGCountdownTimer():
    server: Starlette

    @classmethod
    def initialize(cls) -> None:
        CountdownTimer.initialize()

        cls.server = Starlette()

        # HTTP Routes for CountdownTimer actions
        cls.server.add_route('/v0/countdown/start', CountdownTimerActionEndpoints.start, methods=['GET'])
        cls.server.add_route('/v0/countdown/reset', CountdownTimerActionEndpoints.reset, methods=['GET'])
        cls.server.add_route('/v0/countdown/stop', CountdownTimerActionEndpoints.stop, methods=['GET'])
        cls.server.add_route('/v0/countdown/pause', CountdownTimerActionEndpoints.pause, methods=['GET'])
        cls.server.add_route('/v0/countdown/resume', CountdownTimerActionEndpoints.resume, methods=['GET'])

        # HTTP Routes for Client-Side JavaScript CountdownTimer script
        cls.server.add_route('/v0/client/countdown.js', CountdownTimerFilesEndpoints.countdown_js, methods=['GET'])

        # WebSockets routes for real-time CountdownTimer data exchange
        cls.server.add_websocket_route('/v0/ws/countdown/change', ChangeEndpoint)
        cls.server.add_websocket_route('/v0/ws/countdown/change/subscribers', ChangeSubscribersEndpoint)
