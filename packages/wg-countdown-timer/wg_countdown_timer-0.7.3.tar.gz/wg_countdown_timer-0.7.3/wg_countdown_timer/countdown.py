import json
from asyncio import Event
from time import time
from typing import Set, Any
from apscheduler.schedulers.background import BackgroundScheduler

class SetEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class CountdownTimer():
    scheduler: BackgroundScheduler = None

    seconds: int = 0 # How many seconds left to make a repeat
    timestamp: int = 0 # Timestamp that was made when current second passed
    total_seconds: int = 0 # Total seconds for one repeat
    total_seconds_start_value: int = 10 # Start value of total_seconds for one report (total_seconds will change on seconds_decrements repeats)
    seconds_passed: int = 0 # Seconds passed from the start
    seconds_decrements: Set[int] = {100, 200, 300, 400, 500, 700, 900} # Repeats after which total_seconds will be decreased by 1

    timer_changed_event: Event = None # Used to notify people connected via WebSockets

    repeat: int = 0 # Current repeat
    total_repeats: int = 1000 # Total number of repeats

    breaks: Set[int] = {100, 200, 300, 400, 500, 600, 700, 800, 900} # Repeats after which there will be a break
    break_duration: int = 120 # How many seconds a break will last
    mini_breaks: Set[int] = {50, 150, 250, 350, 450, 550, 650, 750, 850, 950} # Repeats after which there will be a mini-break
    mini_break_duration: int = 10 # How many seconds a mini-break will last

    is_running: bool = False # Is CountdownTimer running
    is_break: bool = False # Is it break or mini-break right now
    is_paused: bool = False # Is CountdownTimer paused

    countdown_data_json: str = '{}' # JSON with current CountdownTimer state data

    @classmethod
    def update_json(cls) -> None:
        cls.countdown_data_json = json.dumps({
            'seconds' : CountdownTimer.seconds,
            'timestamp' : CountdownTimer.timestamp,
            'total_seconds' : CountdownTimer.total_seconds,
            'seconds_passed' : CountdownTimer.seconds_passed,
            'seconds_decrements' : CountdownTimer.seconds_decrements,
            'repeat' : CountdownTimer.repeat,
            'total_repeats' : CountdownTimer.total_repeats,
            'breaks' : CountdownTimer.breaks,
            'break_duration' : CountdownTimer.break_duration,
            'mini_breaks' : CountdownTimer.mini_breaks,
            'mini_break_duration' : CountdownTimer.mini_break_duration,
            'is_running' : CountdownTimer.is_running,
            'is_paused' : CountdownTimer.is_paused,
            'is_break' : CountdownTimer.is_break
        }, cls=SetEncoder)

    @classmethod
    def initialize(cls) -> None:
        if cls.scheduler:
            return

        cls.scheduler = BackgroundScheduler(timezone='Europe/Tallinn')
        cls.scheduler.start()

        cls.update_json()

    @classmethod
    async def wait_for_changes(cls):
        return (await cls.timer_changed_event.wait())

    @classmethod
    def notify_timer_changed(cls) -> None:
        if cls.timer_changed_event:
            cls.update_json()
            cls.timer_changed_event.set()
            cls.timer_changed_event.clear()

    @classmethod
    def countdown_loop(cls) -> None:
        cls.timestamp = time() * 1000
        cls.seconds -= 1
        cls.seconds_passed += 1

        # Exit immediately if there are still seconds for this repeat
        if cls.seconds > 0:
            return

        ### There are no seconds left for this repeat:

        # If we were having a break - stop it and proceed without incrementing repeat counter
        if cls.is_break:
            cls.seconds = cls.total_seconds
            cls.is_break = False
            return

        cls.repeat += 1
        # If this repeat is the last one - stop everything and exit
        if cls.repeat == cls.total_repeats:
            cls.scheduler.remove_all_jobs()
            cls.is_running = False
            return

        # Check if total_seconds should be decremented after this repeat
        if cls.repeat in cls.seconds_decrements:
            cls.total_seconds -= 1

        cls.seconds = cls.total_seconds
        # Check if any of the breaks should be after this repeat
        if cls.repeat in cls.breaks:
            cls.seconds = cls.break_duration
            cls.is_break = True
        elif cls.repeat in cls.mini_breaks:
            cls.seconds = cls.mini_break_duration
            cls.is_break = True

    @classmethod
    def start(cls) -> str:
        if cls.is_running:
            return 'CountdownTimer already running!'

        # Set state
        cls.total_seconds = cls.total_seconds_start_value
        cls.seconds = cls.total_seconds
        cls.seconds_passed = 0
        cls.repeat = 0
        cls.is_running = True
        cls.is_break = False
        cls.is_paused = False

        # Start countdown loop
        cls.scheduler.remove_all_jobs()
        cls.scheduler.add_job(cls.countdown_loop, 'interval', seconds=1)

        # Notify WebSockets subscribers about change (start/restart)
        cls.notify_timer_changed()

        return 'CountdownTimer started'

    @classmethod
    def reset(cls) -> str:
        if not cls.is_running:
            return 'CountdownTimer not running!'

        cls.is_running = False
        cls.start()

        return 'CountdownTimer reset'

    @classmethod
    def stop(cls) -> str:
        if not cls.is_running:
            return 'CountdownTimer not running!'

        # Stop countdown loop
        cls.scheduler.remove_all_jobs()

        # Clear state
        cls.total_seconds = 0
        cls.seconds = 0
        cls.seconds_passed = 0
        cls.repeat = 0
        cls.is_running = False
        cls.is_break = False
        cls.is_paused = False

        # Notify WebSockets subscribers about change (stop)
        cls.notify_timer_changed()

        return 'CountdownTimer stopped'

    @classmethod
    def pause(cls) -> str:
        if not cls.is_running or cls.is_paused:
            return 'CountdownTimer not running or already paused!'

        # Stop countdown loop
        cls.scheduler.remove_all_jobs()
        cls.is_paused = True

        # Notify WebSockets subscribers about change (pause)
        cls.notify_timer_changed()

        return 'CountdownTimer paused'

    @classmethod
    def resume(cls) -> str:
        if not cls.is_running or not cls.is_paused:
            return 'CountdownTimer not running or not paused!'

        # Start countdown loop
        cls.scheduler.remove_all_jobs()
        cls.scheduler.add_job(cls.countdown_loop, 'interval', seconds=1)
        cls.is_paused = False

        # Notify WebSockets subscribers about change (resume)
        cls.notify_timer_changed()

        return 'CountdownTimer resumed'
