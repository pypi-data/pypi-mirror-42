from typing import Union, List

import numpy as np


Points = Union[List, np.ndarray]


class PiecewiseLinearController:

    def __init__(self, time_grid: Points, values: Points):
        self._time_grid = time_grid
        self._values = values

    def generate(self, t: float) -> float:
        for i, t0 in enumerate(self._time_grid[:-1]):
            t1 = self._time_grid[i + 1]
            if t0 <= t <= t1:
                u0, u1 = self._values[i], self._values[i + 1]
                return ((t1 - t) * u0 + (t - t0) * u1) / (t1 - t0)
        raise ValueError(f"Can not generate control for tau <{t}>")

    def __call__(self, *args, **kwargs):
        return self.generate(kwargs.get("t", args[0]))
