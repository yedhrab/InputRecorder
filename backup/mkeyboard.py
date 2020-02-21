import logging
import time

from pynput.keyboard import Controller, Listener, GlobalHotKeys
from decorator import background, delayed, do_delayed

logger = logging.getLogger(__name__)


def hotkey(hotkey: str):
    def trigger(func):
        def inner(*args, **kargs):

            GlobalHotKeys({hotkey: func})


class GlobalHotkeys():
    hotkey = {}

    @staticmethod
    def get_hotkeys(self):
        return self.hotkeys


class KeyboardEvent():

    def __init__(self, key, pressed, duration):
        self.key = key
        self.pressed = pressed
        self.duration = duration

    def __str__(self):
        return "" \
            + "key=" + str(self.key) + " " \
            + "pressed=" + str(self.pressed) + " " \
            + "duration=" + str(self.duration)


class KeyboardController():

    def __init__(self):
        self.controller = Controller()
        logger.debug("Controller tanımlandı")

    def press(self, key):
        self.controller.press(key)
        logger.debug(f"{key} basıldı")

    def release(self, key):
        self.controller.release(key)
        logger.debug(f"{key} bırakıldı")

    def replay(self, events: list):
        for event in events:
            time.sleep(event.duration)

            if event.pressed:
                self.press(event.key)
            else:
                self.release(event.key)


class KeyboardListener():

    def calculate_duration(self):
        old_time, self.last_time = self.last_time, time.time()
        duration = self.last_time - old_time

        return duration

    def for_cannoncial(self, func):
        return lambda key: func(self.listener.canoncial(key))

    def on_press(self, key):
        # TODO: If key is Hotkey, don't save it to events
        self.append_to_event(key, True)

    def on_release(self, key):
        self.append_to_event(key, False)
        pass

    def append_to_event(self, key, pressed):
        duration = self.calculate_duration()

        event = KeyboardEvent(key, pressed, duration)
        self.events.append(event)

        logger.debug(f"{event} kaydediledi")

    def __init__(self):
        self.listener = Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        logger.debug("Listener tanımlandı")

    def record(self, duration=0):
        self.last_time = time.time()
        self.events = []

        self.listener.start()

        logger.info("Dinleyici başlatıldı")

        if duration > 0:
            do_delayed(self.stop_record, duration)

    def stop_record(self):
        self.listener.stop()
        logger.info("Dinleyici sonlandırıldı")

    def play_record(self):
        controller = KeyboardController()
        controller.replay(self.events)

    @background
    def play_record_async(self):
        controller = KeyboardController()
        controller.replay(self.events)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    listener = KeyboardListener()
    listener.record(duration=5)
    listener.play_record()
