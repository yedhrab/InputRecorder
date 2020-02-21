import logging
from pynput.mouse import Listener as MouseListener
import keyboard
import pyautogui

logger = logging.getLogger(__name__)


def record_mouse():

    def save_point(points: list):
        point = pyautogui.position()
        points.append(point)

        logger.info(f"{point=} noktası kaydedildi")

        return points

    def start_mouse_listener(points: list):
        keyboard.remove_hotkey(POINT_HOTKEY)
        keyboard.remove_hotkey(CLOSE_HOTKEY)
        keyboard.add_hotkey(HOTKEY, record_mouse)

        logger.info("Kayıt tamamlandı")

        for point in points:
            pyautogui.moveTo(x=point.x, y=point.y, duration=1)

    keyboard.remove_hotkey(HOTKEY)

    logger.info("Kayıt başlatıldı")
    logger.info(f"{POINT_HOTKEY} ile konumları seçin")
    logger.info(f"{CLOSE_HOTKEY} ile kaydı tamamlayın")

    # Capture mouse points
    points = []
    keyboard.add_hotkey(POINT_HOTKEY, save_point, args=(points,))
    keyboard.add_hotkey(CLOSE_HOTKEY, start_mouse_listener, args=(points,))


HOTKEY = "windows+ctrl+shift+r"
POINT_HOTKEY = "ctrl"
CLOSE_HOTKEY = "esc"

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

keyboard.add_hotkey(HOTKEY, record_mouse)
keyboard.wait()
