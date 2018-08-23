from gpiozero import Button
from time import sleep
from lib.floasis.config import *

red_button = Button(BUTTON_PINID_RED, bounce_time=0.05)
blu_button = Button(BUTTON_PINID_BLU, bounce_time=0.05)
grn_button = Button(BUTTON_PINID_GRN, bounce_time=0.05)
whi_button = Button(BUTTON_PINID_WHI, bounce_time=0.05)

def set_button_callbacks(_btn, name):
    def __callback(_status):
        def __fn():
            print(name, _status, _btn.value)
        return __fn
    _btn.when_pressed = __callback('pressed')
    _btn.when_released = __callback('depressed')
    return _btn

set_button_callbacks(grn_button, 'grn')
set_button_callbacks(blu_button, 'blu')
set_button_callbacks(red_button, 'red')
set_button_callbacks(whi_button, 'whi')


while True:
    sleep(0.1)
