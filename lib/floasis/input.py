from gpiozero import LED, Button
from time import sleep

red_led = LED(21)
blue_led = LED(26)
grn_led = LED(19)
whi_led = LED(20)
button_up = Button(18)
button_down = Button(25)
button_left = Button(4)
button_right = Button(24)
pin_a = Button(5,pull_up=True)
pin_b = Button(6,pull_up=True)

class Incrementor(object):

    def __init__(self, pin_a, pin_b):
        self._cnt = 0
        self._ascending = True
        self.pin_a = pin_a
        self.pin_b = pin_b

        self.pin_a.when_pressed = self.ccw
        self.pin_b.when_pressed = self.cw

    def revert_check(self):
        if self._cnt > 100:
            self._ascending = not self._ascending
            print('REVERT {i}'.format(i=self._ascending))
        elif self._cnt < -100:
            self._ascending = not self._ascending
            print('REVERT {i}'.format(i=self._ascending))

    def ccw(self):
        if pin_b.is_pressed:
            self.revert_check()
            self._cnt = self._cnt + 1 if self._ascending else self._cnt - 1
            print('ccw {i}'.format(i=self._cnt))

    def cw(self):
        if pin_a.is_pressed:
            self.revert_check()
            self._cnt = self._cnt - 1 if self._ascending else self._cnt + 1
            print('cw {i}'.format(i=self._cnt))

    @property
    def count(self):
        return self._cnt

incrementor = Incrementor(pin_a, pin_b)

while True:
    if button_up.is_pressed:
        print("up")
        grn_led.on()
    elif button_left.is_pressed:
        print("left")
        blue_led.on()
    elif button_down.is_pressed:
        print("down")
        red_led.on()
    elif button_right.is_pressed:
        print("right")
        whi_led.on()
    else:
        grn_led.off()
        blue_led.off()
        red_led.off()
        whi_led.off()

    sleep(0.02)
