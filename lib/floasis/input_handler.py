import logging
from gpiozero import LED, Button
from time import sleep


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Incrementor(object):

    def __init__(self, pin_a, pin_b, update_cnt):
        self._cnt = 0
        self._ascending = True
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.update_cnt = update_cnt

        self.pin_a.when_pressed = self.ccw
        self.pin_b.when_pressed = self.cw

    def revert_check(self):
        if self._cnt > 100:
            self._ascending = not self._ascending
            logger.debug('REVERT {i}'.format(i=self._ascending))
        elif self._cnt < -100:
            self._ascending = not self._ascending
            logger.debug('REVERT {i}'.format(i=self._ascending))

    def ccw(self):
        if self.pin_b.is_pressed:
            self.revert_check()
            self._update(self._cnt + 1 if self._ascending else self._cnt - 1)
            logger.debug('ccw {i}'.format(i=self._cnt))

    def cw(self):
        if self.pin_a.is_pressed:
            self.revert_check()
            self._update(self._cnt - 1 if self._ascending else self._cnt + 1)
            logger.debug('cw {i}'.format(i=self._cnt))

    def _update(self, newval):
        self._cnt = newval
        if self.update_cnt:
            self.update_cnt(self._cnt)


    @property
    def count(self):
        return self._cnt


class InputHandler(object):

    def __init__(self,
                 rotary_callback=None,
                 left_callback=None,
                 right_callback=None,
                 down_callback=None,
                 up_callback=None,
                 ):
        self.red_led = LED(21)
        self.blue_led = LED(26)
        self.yel_led = LED(19)
        self.whi_led = LED(20)
        self.button_up = Button(18)
        self.button_down = Button(25)
        self.button_left = Button(4)
        self.button_right = Button(24)
        self.pin_a = Button(5, pull_up=True)
        self.pin_b = Button(6, pull_up=True)

        self.incrementor = Incrementor(self.pin_a, self.pin_b,
                                       update_cnt=rotary_callback)

        self.left_callback = left_callback
        self.right_callback = right_callback
        self.down_callback = down_callback
        self.up_callback = up_callback

    def check_input_changes(self):
        if self.button_up.is_pressed:
            logger.debug("up")
            if self.up_callback:
                self.up_callback()
            if self.yel_led:
                self.yel_led.on()
        elif self.button_left.is_pressed:
            logger.debug("left")
            if self.left_callback:
                self.left_callback()
            if self.blue_led:
                self.blue_led.on()
        elif self.button_down.is_pressed:
            logger.debug("down")
            if self.down_callback:
                self.down_callback()
            if self.red_led:
                self.red_led.on()
        elif self.button_right.is_pressed:
            logger.debug("right")
            if self.right_callback:
                self.right_callback()
            if self.whi_led:
                self.whi_led.on()
        else:
            self.yel_led.off()
            self.blue_led.off()
            self.red_led.off()
            self.whi_led.off()


if __name__ == '__main__':
    input_handler = InputHandler()
    while True:
        input_handler.check_input_changes()
        sleep(0.02)
