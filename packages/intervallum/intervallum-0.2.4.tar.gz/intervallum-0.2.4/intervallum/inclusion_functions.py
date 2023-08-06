from typing import Callable, Union, List

import numpy as np

from intervallum.box import Box
from intervallum.interval import Interval


class RS_SubinclusionFunction:

    def __init__(self, f: Callable[[Union[np.ndarray, List[float]]], Union[np.ndarray, float]], number_of_samples: int):
        self._number_of_samples = number_of_samples
        self._f = f

    def __call__(self, x: Box) -> "Interval":
        def generate_point(b: Box) -> np.ndarray:
            return np.random.uniform(low=b.lb, high=b.ub)
        points = [generate_point(x) for _ in range(self._number_of_samples)]
        values = list(map(self._f, points))
        return Interval(min(values), max(values))
