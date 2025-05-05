"""Trench Map
https://adventofcode.com/2021/day/20
"""

import numpy as np
from scipy.signal import convolve2d


class ImageEnhancementAutomata:
    def __init__(self, state: np.ndarray, rule: np.ndarray):
        self.state = state
        self.rule = rule
        self.boundary_value = 0
        self.vision = 2 ** (np.arange(9).reshape((3, 3)))
        self.vfunc = np.vectorize(lambda x: self.rule[x])

    def __repr__(self):
        ret_val = ""
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                ret_val += "#" if self.state[i, j] else "."
            ret_val += "\n"

        return ret_val

    def get_next_boundary_value(self, val):
        return self.rule[val * (len(self.rule) - 1)]

    def update(self):
        self.state = self.vfunc(
            convolve2d(
                self.state,
                self.vision,
                mode="full",
                boundary="fill",
                fillvalue=int(self.boundary_value),
            )
        )
        self.boundary_value = self.get_next_boundary_value(int(self.boundary_value))

    def count_state(self):
        return np.sum(self.state)


def parse_input(s: str):
    image_lines = s.split("\n")
    algo_mode = True
    algorithm = None
    image_list: list[list[int]] = []

    for image_line in image_lines:
        if algo_mode:
            algorithm = [True if x == "#" else False for x in image_line.strip()]
            algo_mode = False
        elif len(image_line.strip()) > 0 and not algo_mode:
            image_list.append([True if x == "#" else False for x in image_line.strip()])

    return np.array(image_list, dtype=bool), algorithm


def solve_a(s) -> int:
    image, algorithm = parse_input(s)
    image_ca = ImageEnhancementAutomata(image, algorithm)
    image_ca.update()
    image_ca.update()
    return image_ca.count_state()


def solve_b(s) -> str:
    image, algorithm = parse_input(s)
    image_ca = ImageEnhancementAutomata(image, algorithm)
    for _ in range(50):
        image_ca.update()
    return f"{image_ca.count_state()}"
