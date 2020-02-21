import keyboard

source_text = "test"
replacement = '/b'*(len(source_text)+1) + "HEHE"


def callback(): return keyboard.write(replacement)
