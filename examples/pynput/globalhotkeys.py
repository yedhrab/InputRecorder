from pynput import keyboard


def test1():
    def on_activate_h():
        print('<ctrl>+<alt>+h pressed')

    def on_activate_i():
        print('<ctrl>+<alt>+i pressed')

    with keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+h': on_activate_h,
            '<ctrl>+<alt>+i': on_activate_i}) as h:
        h.join()


def test2():
    from pynput import keyboard

    def on_press(key):
        print(key)
        hotkey.press(key)

    def on_activate():
        print('Global hotkey activated!')

    def for_canonical(f):
        return lambda k: f(l.canonical(k))

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<alt>+h'),
        on_activate)

    with keyboard.Listener(
            on_press=on_press,
            on_release=for_canonical(hotkey.release)) as l:
        l.join()

    hotkey.press(l.canonical())


test2()
