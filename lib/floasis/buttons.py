from gpiozero import Button
from time import sleep

red_button = Button(21, bounce_time=0.05)
blue_button = Button(26, bounce_time=0.05)
grn_button = Button(19, bounce_time=0.05)
whi_button = Button(20, bounce_time=0.05)

def set_button_callbacks(_btn, name):
    def __callback(_status):
        def __fn():
            print(name, _status, _btn.value)
        return __fn
    _btn.when_pressed = __callback('pressed')
    _btn.when_released = __callback('depressed')
    return _btn

set_button_callbacks(grn_button, 'grn')
set_button_callbacks(blue_button, 'blue')
set_button_callbacks(red_button, 'red')
set_button_callbacks(whi_button, 'whi')

# 
# grn_button.when_pressed = set_button_callbacks('pressed grn\n')
# grn_button.when_released = set_button_callbacks('depressed grn\n')
# 
# blue_button.when_pressed = set_button_callbacks('pressed blue\n')
# blue_button.when_released = set_button_callbacks('depressed blue\n')
# 
# red_button.when_pressed = set_button_callbacks('pressed red\n')
# red_button.when_released = set_button_callbacks('depressed red\n')
# 
# whi_button.when_pressed = set_button_callbacks('pressed whi\n')
# whi_button.when_released = set_button_callbacks('depressed whi\n')
# 

while True:
    sleep(0.1)
