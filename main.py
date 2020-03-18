import logging
import time

import coloredlogs
import keyboard
import mouse
from keyboard._keyboard_event import KEY_DOWN, KeyboardEvent
from mouse._mouse_event import UP, ButtonEvent, MoveEvent, WheelEvent

from background import background

coloredlogs.install(level="DEBUG")
logger = logging.getLogger(__name__)


class Hotkey:
    def __init__(self, hotkey, callback, args=()):
        self.hotkey = hotkey
        self.callback = callback
        self.args = args


class InputController:
    def __init__(self):

        self.events = []
        self.hotkeys = []

        self.recording = False

        # To remove hotkey keys
        self.first_event_ix = None
        self.last_event_ix = None

        self.base_keys = "windows+ctrl"

    def reset_records(self):
        del self.events
        self.events = Event()

    def add_event(self, event):
        self.events.append(event)

        logger.debug(f"{event=} eklendi")

    @background
    def _record_mouse(self):
        self.mouse_hook = mouse.hook(self.add_event)

        logger.info("Mouse kaydı başlatıldı")

    @background
    def _record_keyboard(self):
        self.keyboard_hook = keyboard.hook(self.add_event)

        logger.info("Klavye kaydı başlatıldı")

    @background
    def _play_mouse(self):
        logger.info("Mouse kaydı oynatılıyor")

        mouse.play(self.events.mouse_events)

    @background
    def _play_keyboard(self):
        logger.info("Klavye kaydı oynatılıyor")

        keyboard.play(self.events.keyboard_events)

    def _record(self):
        self._record_keyboard()
        self._record_mouse()

        self.recording = True

        logger.info("Kayıt başlatıldı")

    def record(self):
        # Avoid multiple recording
        if self.recording:
            logger.warning("Zaten kayıt yapılmakta")
            return

        self._record()

    def record_with_hotkey(self, start_keys: str, stop_keys: str):
        start_hotkey = Hotkey(start_keys, self.record)
        stop_hotkey = Hotkey(stop_keys, self.stop_recording)

        self.add_hotkey(start_hotkey)
        self.add_hotkey(stop_hotkey)

        # To remove hotkey keys
        self.first_event_ix = len(start_keys.split("+")) + 1
        self.last_event_ix = -(len(stop_keys.split("+")) + 1)

    def _trim_event(self):
        self.events = self.events[self.first_event_ix : self.last_event_ix]

    def _stop_recording(self):
        keyboard.unhook(self.keyboard_hook)
        mouse.unhook(self.mouse_hook)

        self.recording = False

        logger.info("Kayıt tamamlandı")

    def stop_recording(self):
        if not self.recording:
            logger.warning("Aktif kayıt bulunamadı")
            return

        self._stop_recording()
        self._trim_event()

    def _play(self, speed_factor=1.0, include_clicks=True, include_moves=True, include_wheel=True):
        # For hotkey management
        state = keyboard.stash_state()

        last_time = None
        for event in self.events:
            if speed_factor > 0 and last_time is not None:
                time.sleep((event.time - last_time) / speed_factor)
            last_time = event.time

            if isinstance(event, KeyboardEvent):
                key = event.scan_code or event.name
                keyboard.press(key) if event.event_type == KEY_DOWN else keyboard.release(key)

            if isinstance(event, ButtonEvent) and include_clicks:
                if event.event_type == UP:
                    mouse.release(event.button)
                else:
                    mouse.press(event.button)
            elif isinstance(event, MoveEvent) and include_moves:
                mouse.move(event.x, event.y)
            elif isinstance(event, WheelEvent) and include_wheel:
                mouse.wheel(event.delta)

        # For hotkey management
        keyboard.restore_modifiers(state)

    def play_record(self):
        if self.events:
            logger.info("Kayıt oynatılıyor")
            self._play()
            logger.info("Kaydı oynatma tamamlandı")

            return True
        else:
            return False

    @background
    def play_record_infinite(self):
        while self.play_record():
            pass

    def wait_keyboard(self):
        keyboard.wait()

    def _add_hotkey(self, hotkey):
        keyboard.add_hotkey(hotkey.hotkey, hotkey.callback, hotkey.args, suppress=True, trigger_on_release=True)

    def add_hotkey(self, hotkey: Hotkey):
        self.hotkeys.append(hotkey)
        self._add_hotkey(hotkey)

    def add_hotkeys(self, hotkeys):
        for hotkey in hotkeys:
            self.add_hotkey(hotkey)

    def create_hotkey(self, key_string):
        return self.base_keys + "+" + key_string


controller = InputController()
controller.record_with_hotkey(controller.create_hotkey("r"), controller.create_hotkey("s"))
controller.add_hotkeys(
    [
        Hotkey(controller.create_hotkey("p"), controller.play_record_infinite),
        Hotkey(controller.create_hotkey("e"), exit),
    ]
)
controller.wait_keyboard()
