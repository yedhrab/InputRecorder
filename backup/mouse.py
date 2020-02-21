"""Mouse recoder & listener

TODO: Threading
"""

import logging
import time
import threading

from pyautogui import moveTo
from pynput.mouse import Controller, Listener
from decorator import background, delayed, do_delayed


logger = logging.getLogger(__name__)


class MouseEvent():

    def __init__(self, x, y, button, pressed, duration):
        self.x = x
        self.y = y
        self.button = button
        self.pressed = pressed
        self.duration = duration

    def __str__(self):
        return "" \
            + "x=" + str(self.x) + " " \
            + "y=" + str(self.y) + " " \
            + "button=" + str(self.button) + " " \
            + "pressed=" + str(self.pressed) + " " \
            + "duration=" + str(self.duration)

    def replay(self, controller):
        moveTo(self.x, self.y, self.duration)

        if self.pressed:
            controller.press(self.button)
        else:
            controller.release(self.button)


class MouseController():

    def __init__(self):
        self.controller = Controller()
        logger.debug("Controller tanımlandı")

    def press(self, button):
        self.controller.press(button)
        logger.debug(f"{button} basıldı")

    def release(self, button):
        self.controller.release(button)
        logger.debug(f"{button} bırakıldı")

    def replay(self, events: list):
        for event in events:
            moveTo(event.x, event.y, event.duration)

            if event.pressed:
                self.press(event.button)
            else:
                self.release(event.button)


class MouseListener():

    def calculate_duration(self):
        old_time, self.last_time = self.last_time, time.time()
        duration = self.last_time - old_time

        return duration

    def on_move(self, x, y):
        pass

    def on_click(self, x, y, button, pressed):
        self.append_click_to_event(x, y, button, pressed)

    def on_scroll(self, x, y, dx, dy):
        pass

    def append_click_to_event(self, x, y, button, pressed):
        duration = self.calculate_duration()

        event = MouseEvent(x, y, button, pressed, duration)
        self.events.append(event)

        logger.debug(f"{event} kaydedildi")

    def __init__(self):
        self.listener = Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )

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
        controller = MouseController()
        controller.replay(self.events)

    @background
    def play_record_async(self):
        self.play_record()

    def export_record(self):
        logger.warn("Henüz desteklenmiyor")
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    listener = MouseListener()
    listener.record(duration=5)
    listener.play_record()
