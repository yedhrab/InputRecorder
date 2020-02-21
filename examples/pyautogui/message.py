import pyautogui

pyautogui.alert('This is an alert box.')
# 'OK'
pyautogui.confirm('Shall I proceed?')
# 'Cancel'
pyautogui.confirm('Enter option.', buttons=['A', 'B', 'C'])
# 'B'
pyautogui.prompt('What is your name?')
# 'Al'
pyautogui.password('Enter password (text will be hidden)')
# 'swordfish'
