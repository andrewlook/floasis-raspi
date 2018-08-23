from gpiozero import Button
from time import sleep
from lib.floasis.config import *
from lib.floasis.inputs.incr_mgr import IncrementorManager

DEFAULT_HOLD_MGR_PARAMS = dict(
    min_value=0.2,
    max_value=2.0,
    step_size=0.1,
    loop=True,
)
DEFAULT_PRESS_MGR_PARAMS = dict(
    min_value=1.0,
    max_value=4.0,
    step_size=1.0,
    loop=True,
)

class ButtonManager(object):

    def __init__(self,
                 btn_red=None,
                 btn_blu=None,
                 btn_grn=None,
                 btn_whi=None):
        self.btn_red = btn_red
        self.btn_blu = btn_blu
        self.btn_grn = btn_grn
        self.btn_whi = btn_whi

        self.red_hold_mgr = IncrementorManager(name='red_hold',
                                               **DEFAULT_HOLD_MGR_PARAMS)
        self.blu_hold_mgr = IncrementorManager(name='blu_hold',
                                               **DEFAULT_HOLD_MGR_PARAMS)
        self.grn_hold_mgr = IncrementorManager(name='grn_hold',
                                               **DEFAULT_HOLD_MGR_PARAMS)
        self.whi_hold_mgr = IncrementorManager(name='whi_hold',
                                               **DEFAULT_HOLD_MGR_PARAMS)
        self.btn_red.when_held = self.red_hold_mgr.update_callback(ORDER_UP)
        self.btn_grn.when_held = self.grn_hold_mgr.update_callback(ORDER_UP)
        self.btn_blu.when_held = self.blu_hold_mgr.update_callback(ORDER_UP)
        self.btn_whi.when_held = self.whi_hold_mgr.update_callback(ORDER_UP)

        self.red_press_mgr = IncrementorManager(name='red_press',
                                               **DEFAULT_PRESS_MGR_PARAMS)
        self.blu_press_mgr = IncrementorManager(name='blu_press',
                                               **DEFAULT_PRESS_MGR_PARAMS)
        self.grn_press_mgr = IncrementorManager(name='grn_press',
                                               **DEFAULT_PRESS_MGR_PARAMS)
        self.whi_press_mgr = IncrementorManager(name='whi_press',
                                               **DEFAULT_PRESS_MGR_PARAMS)
        self.btn_red.when_pressed = self.red_press_mgr.update_callback(ORDER_UP)
        self.btn_grn.when_pressed = self.grn_press_mgr.update_callback(ORDER_UP)
        self.btn_blu.when_pressed = self.blu_press_mgr.update_callback(ORDER_UP)
        self.btn_whi.when_pressed = self.whi_press_mgr.update_callback(ORDER_UP)
    
    @property
    def red_hold(self):
        return self.red_hold_mgr.val

    @property
    def red_press(self):
        return self.red_press_mgr.val
    
    @property
    def blu_hold(self):
        return self.blu_hold_mgr.val

    @property
    def blu_press(self):
        return self.blu_press_mgr.val
    

    @property
    def grn_hold(self):
        return self.grn_hold_mgr.val

    @property
    def grn_press(self):
        return self.grn_press_mgr.val
    
    @property
    def whi_hold(self):
        return self.whi_hold_mgr.val

    @property
    def whi_press(self):
        return self.whi_press_mgr.val


    @property
    def red_down(self):
        return self.btn_red.is_pressed

    @property
    def grn_down(self):
        return self.btn_grn.is_pressed
    
    @property
    def blu_down(self):
        return self.btn_blu.is_pressed

    @property
    def whi_down(self):
        return self.btn_whi.is_pressed



if __name__ == '__main__':
    btn_args = dict(
        bounce_time=0.05,
        hold_time=0.5,
        hold_repeat=True,
    )
    red_button = Button(BUTTON_PINID_RED, **btn_args)
    blu_button = Button(BUTTON_PINID_BLU, **btn_args)
    grn_button = Button(BUTTON_PINID_GRN, **btn_args)
    whi_button = Button(BUTTON_PINID_WHI, **btn_args)

    m = ButtonManager(btn_red=red_button,
                      btn_grn=grn_button,
                      btn_blu=blu_button,
                      btn_whi=whi_button)

    cnt = 0
    while True:
        cnt += 1
        if cnt % 10 == 0:
            print("down:\tr={r}\tg={g}\tb={b}\tw={w}".format(r=m.red_down,
                                                             g=m.grn_down,
                                                             b=m.blu_down,
                                                             w=m.whi_down))
            print("hold:\tr={r}\tg={g}\tb={b}\tw={w}".format(r=m.red_hold,
                                                             g=m.grn_hold,
                                                             b=m.blu_hold,
                                                             w=m.whi_hold))
            print("press:\tr={r}\tg={g}\tb={b}\tw={w}".format(r=m.red_press,
                                                              g=m.grn_press,
                                                              b=m.blu_press,
                                                              w=m.whi_press))
        sleep(0.1)
