from typing import List, Callable

import numpy as np

from intervallum.interval import IntervalNumber
from intervallum.box import Box, BoxVector


Func = Callable[[IntervalNumber, BoxVector], BoxVector]


class SatelliteStabilization:
    
    def __init__(self, u1: Func, u2: Func, u3: Func):
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3
    
    def _model_eq(self, t: IntervalNumber, state: BoxVector) -> List[IntervalNumber]:
        [p, q, r, _] = state
        u1 = self.u1(t, state)
        u2 = self.u2(t, state)
        u3 = self.u3(t, state)
        return [
            u1 / 6.0,
            u2 - 0.2 * p * r,
            0.2 * (u3 + p * q),
            abs(u1) + abs(u2) + abs(u3)
        ]
    
    def model_eq_np(self, t: IntervalNumber, state: BoxVector) -> BoxVector:
        return np.array(self._model_eq(t, state))
    
    # not used not
    # def model_eq_interval(self, t: IntervalNumber, state: BoxVector) -> BoxVector:
    #     return Box(*self._model_eq(t, state))
