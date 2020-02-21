import pyautogui
# Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
screenWidth, screenHeight = pyautogui.size()
# Returns two integers, the x and y of the mouse cursor's current position.
currentMouseX, currentMouseY = pyautogui.position()
pyautogui.moveTo(100, 150)  # Move the mouse to the x, y coordinates 100, 150.
pyautogui.click()  # Click the mouse at its current location.
pyautogui.click(200, 220)  # Click the mouse at the x, y coordinates 200, 220.
# Move mouse 10 pixels down, that is, move the mouse relative to its current position.
pyautogui.move(None, 10)
pyautogui.doubleClick()  # Double click the mouse at the
# Use tweening/easing function to move mouse over 2 seconds.
pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)
# Type with quarter-second pause in between each key.
pyautogui.write('Hello world!', interval=0.25)
pyautogui.press('esc')  # Simulate pressing the Escape key.
pyautogui.keyDown('shift')
pyautogui.write(['left', 'left', 'left', 'left', 'left', 'left'])
pyautogui.keyUp('shift')
pyautogui.hotkey('ctrl', 'c')
