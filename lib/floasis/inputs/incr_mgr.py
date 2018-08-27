
from lib.floasis.config import *

class IncrementorManager(object):

    def __init__(self,
                 default_value=DEFAULT_VAL,
                 max_value=DEFAULT_MAX_VAL,
                 min_value=DEFAULT_MIN_VAL,
                 step_size=DEFAULT_STEP_SIZE,
                 debug=True):
        self.value = DEFAULT_VAL
        self.min_value = min_value
        self.max_value = max_value
        self.step_size = step_size
        self.debug = debug

    def _log(self, msg):
        if self.debug:
            print(msg)

    def update(self, order):
        sign = 1.0 if order == ORDER_UP else -1.0
        delta = sign * self.step_size
        newval = self.value + delta
        # check boundary conditions
        if newval <= self.max_value and newval >= self.min_value:
            self.value = newval
            self._log('value = {s}, order = {o}'.format(s=self.value, o=order))
        else:
            # # TODO(look): better boundary condition handling?
            #        if self.order == ORDER_UP and self.value >= MAX_SCALE:
            #            self.order = ORDER_DOWN
            #        elif self.order == ORDER_DOWN and self.value <= MIN_SCALE:
            #            self.order = ORDER_UP
            self._log('newval = {n} outside bounds; keep value {v}'
                      .format(n=newval, v=self.value))

    def update_callback(self, order):
        def __callback():
            self.update(order)
        return __callback
