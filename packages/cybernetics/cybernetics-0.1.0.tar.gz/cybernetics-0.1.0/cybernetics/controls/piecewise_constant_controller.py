from typing import Union, List

import numpy as np


Points = Union[List, np.ndarray]


class PiecewiseConstantController:

    def __init__(self, time_grid: Points, values: Points):
        self._time_grid = list(time_grid) + [np.inf]
        self._values = values

    def generate(self, t: float) -> float:
        for i, t_prev in enumerate(self._time_grid[:-1]):
            if t_prev <= t < self._time_grid[i + 1]:
                return self._values[i]
        raise ValueError(f"Can not generate control for tau <{t}>")

    def __call__(self, *args, **kwargs):
        return self.generate(kwargs.get("t", args[0]))
