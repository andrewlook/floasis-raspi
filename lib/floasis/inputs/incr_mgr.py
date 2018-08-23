
from lib.floasis.config import *

EPSILON = 1e-4

class IncrementorManager(object):

    def __init__(self,
                 default_value=DEFAULT_VAL,
                 max_value=DEFAULT_MAX_VAL,
                 min_value=DEFAULT_MIN_VAL,
                 step_size=DEFAULT_STEP_SIZE,
                 debug=True,
                 name='',
                 loop=False,
                ):
        self.val = DEFAULT_VAL
        self.min_value = min_value
        self.max_value = max_value
        self.step_size = step_size
        self.debug = debug
        self.name = name
        self.loop = loop

    def _log(self, msg):
        if self.debug:
            print(msg)

    def update(self, order):
        sign = 1.0 if order == ORDER_UP else -1.0
        delta = sign * self.step_size
        newval = self.val + delta
        # check boundary conditions
        if newval <= self.max_value + EPSILON \
                and newval >= self.min_value - EPSILON:
            self.val = newval
            self._log('{n} value = {s}, order = {o}'
                      .format(n=self.name, s=self.val, o=order))
        elif self.loop:
            self.val = self.min_value
        else:
            # # TODO(look): better boundary condition handling?
            #        if self.order == ORDER_UP and self.val >= MAX_SCALE:
            #            self.order = ORDER_DOWN
            #        elif self.order == ORDER_DOWN and self.val <= MIN_SCALE:
            #            self.order = ORDER_UP
            self._log('newval = {n} outside bounds; keep value {v}'
                      .format(n=newval, v=self.val))

    def update_callback(self, order):
        def __callback():
            self.update(order)
        return __callback
