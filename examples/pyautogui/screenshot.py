import pyautogui

im1 = pyautogui.screenshot()
im1.save('my_screenshot.png')
im2 = pyautogui.screenshot('my_screenshot2.png')

# returns (left, top, width, height) of matching region
button7location = pyautogui.locateOnScreen('button.png')
button7location
(1416, 562, 50, 41)
buttonx, buttony = pyautogui.center(button7location)
buttonx, buttony
(1441, 582)
pyautogui.click(buttonx, buttony)  # clicks the center of where the button was found

buttonx, buttony = pyautogui.locateCenterOnScreen(
    'button.png')  # returns (x, y) of matching region
buttonx, buttony
(1441, 582)
pyautogui.click(buttonx, buttony)  # clicks the center of where the button was found
