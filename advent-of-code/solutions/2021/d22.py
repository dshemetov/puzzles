# /// script
# requires-python = ">=3.14"
# dependencies = ["more-itertools", "numpy"]
# ///
"""22. Reactor Reboot https://adventofcode.com/2021/day/22

The problem involves boolean operations on rectangular regions of 2D space
https://en.wikipedia.org/wiki/Boolean_operations_on_polygons
"""

import re
import sys
import time
from collections.abc import Generator
from copy import deepcopy
from itertools import combinations, pairwise, product
from math import inf

import numpy as np
from more_itertools import flatten


def apply_until_fixed(func):
    """Repeatedly compose a function until the output does not change.

    Assumes func has a single non-keyword argument.
    """

    def new_func(*args, **kwargs):
        new_val, old_val = func(*args, **kwargs), object()
        while new_val != old_val:
            new_val, old_val = func(new_val, **kwargs), new_val
        return new_val

    return new_func


def part_a(s: str) -> int:
    slices = parse_input(s)
    xmin_ = ymin_ = zmin_ = -50
    xmax_ = ymax_ = zmax_ = 50
    xsize_ = xmax_ - xmin_ + 1
    ysize_ = ymax_ - ymin_ + 1
    zsize_ = zmax_ - zmin_ + 1
    region = np.zeros((xsize_, ysize_, zsize_), dtype=bool)
    for cube_slice in slices:
        x, y, z = cube_slice.x, cube_slice.y, cube_slice.z
        x_s, x_e = max(x.start + 50, 0), min(x.stop + 50, 101)
        y_s, y_e = max(y.start + 50, 0), min(y.stop + 50, 101)
        z_s, z_e = max(z.start + 50, 0), min(z.stop + 50, 101)
        region[x_s:x_e, y_s:y_e, z_s:z_e] = cube_slice.on

    return np.sum(region)


class NooiceSlice:
    """A class implementing the algebra of left-closed integer intervals [a, b).

    Examples:
    >>> assert NooiceSlice(2, 5) | NooiceSlice(4, 7) == NooiceSlice(2, 7)
    >>> assert NooiceSlice(4, 7) | NooiceSlice(2, 5) == NooiceSlice(2, 7)
    >>> assert NooiceSlice(2, 4) | NooiceSlice(4, 7) == NooiceSlice(2, 7)
    >>> assert NooiceSlice(2, 5) | NooiceSlice(0, 0) == NooiceSlice(2, 5)
    >>> assert NooiceSlice(2, 5) & NooiceSlice(4, 7) == NooiceSlice(4, 5)
    >>> assert NooiceSlice(4, 7) & NooiceSlice(2, 5) == NooiceSlice(4, 5)
    >>> assert NooiceSlice(2, 5) & NooiceSlice(1, 10) == NooiceSlice(2, 5)
    >>> assert NooiceSlice(2, 5) & NooiceSlice() == NooiceSlice(2, 5)
    >>> assert NooiceSlice(2, 5) & NooiceSlice(5, 10) == NooiceSlice(0, 0)
    >>> assert not NooiceSlice(2, 5) < NooiceSlice(4, 7)
    >>> assert NooiceSlice(2, 5) < NooiceSlice(1, 10)
    >>> assert NooiceSlice(2, 5) < NooiceSlice(2, 10)
    >>> assert NooiceSlice(2, 5) < NooiceSlice(1, 5)
    >>> assert not NooiceSlice(2, 5) < NooiceSlice(2, 5)
    >>> assert NooiceSlice(2, 5) <= NooiceSlice(2, 5)
    >>> assert not NooiceSlice(1, 5) <= NooiceSlice(2, 5)
    >>> assert not NooiceSlice(2, 5).is_empty
    >>> assert NooiceSlice(0, 0).is_empty
    >>> assert not NooiceSlice(2, 5).is_singleton
    >>> assert NooiceSlice(2, 3).is_singleton
    >>> assert not NooiceSlice(2, 5).disjoint(NooiceSlice(4, 7))
    >>> assert NooiceSlice(2, 5).disjoint(NooiceSlice(5, 7))
    >>> assert 3 in NooiceSlice(2, 5)
    >>> assert 3 not in NooiceSlice(4, 5)
    >>> assert 2 in NooiceSlice(2, 3)
    >>> assert 3 not in NooiceSlice(2, 3)
    >>> assert NooiceSlice(2, 5).adjacent(NooiceSlice(5, 7))
    >>> assert not NooiceSlice(2, 5).adjacent(NooiceSlice(6, 7))
    >>> assert NooiceSlice(2, 5).combine(NooiceSlice(5, 8)) == NooiceSlice(2, 8)
    >>> assert NooiceSlice(2, 5).to_slice() == slice(2, 5)
    """

    def __init__(self, start: int = -inf, stop: int = inf):
        self.check_start_stop(start, stop)
        self.__start = start
        self.__stop = stop

    @classmethod
    def check_start_stop(cls, start: int | None, stop: int | None) -> None:
        if stop < start:
            raise ValueError(f"Stop ({stop}) should not be less than start ({start}).")

    @classmethod
    def from_slice(cls, slc: slice) -> "NooiceSlice":
        start = slc.start if slice.start is not None else -inf
        stop = slc.stop if slice.stop is not None else inf
        return NooiceSlice(start, stop)

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, start: int):
        self.check_start_stop(start, self.stop)
        self.__start = start

    @property
    def stop(self):
        return self.__stop

    @stop.setter
    def stop(self, stop: int):
        self.check_start_stop(self.start, stop)
        self.__stop = stop

    @property
    def is_empty(self):
        return self.stop == self.start

    @property
    def is_singleton(self):
        return self.start == self.stop - 1

    def shift_cp(self, offset: int) -> "NooiceSlice":
        return NooiceSlice(self.__start + offset, self.__stop + offset)

    def disjoint(self, other: "NooiceSlice") -> bool:
        return bool(self.stop <= other.start or other.stop <= self.start)

    def adjacent(self, other: "NooiceSlice") -> bool:
        return self.stop == other.start or self.start == other.stop

    def __or__(self, other: "NooiceSlice") -> "NooiceSlice":
        if self.start <= other.start <= self.stop <= other.stop:
            return NooiceSlice(self.start, other.stop)
        if other.start <= self.start <= other.stop <= self.stop:
            return NooiceSlice(other.start, self.stop)
        if self <= other:
            return other
        if other <= self:
            return self
        if self.is_empty:
            return other
        if other.is_empty:
            return self
        if self.disjoint(other):
            raise NotImplementedError("A union of disjoint NooiceSlices is not a NooiceSlice.")

    def union(self, other: "NooiceSlice") -> "NooiceSlice":
        return self | other

    def __and__(self, other: "NooiceSlice") -> "NooiceSlice":
        if self.start <= other.start < self.stop <= other.stop:
            return NooiceSlice(other.start, self.stop)
        if other.start <= self.start < other.stop <= self.stop:
            return NooiceSlice(self.start, other.stop)
        if self <= other:
            return self
        if other <= self:
            return other
        return NooiceSlice(0, 0)

    def intersect(self, other: "NooiceSlice") -> "NooiceSlice":
        return self & other

    def __eq__(self, other: "NooiceSlice") -> bool:
        return self.start == other.start and self.stop == other.stop

    def __lt__(self, other: "NooiceSlice") -> bool:
        return (other.start <= self.start <= self.stop < other.stop) or (
            other.start < self.start <= self.stop <= other.stop
        )

    def __le__(self, other: "NooiceSlice") -> bool:
        return other.start <= self.start <= self.stop <= other.stop

    def __contains__(self, i: int) -> bool:
        return self.start <= i < self.stop

    def combine(self, other: "NooiceSlice") -> "NooiceSlice":
        if not self.adjacent(other):
            raise NotImplementedError("Can't combine non-adjacent NiceSlices.")
        return self | other

    def to_slice(self) -> slice:
        start = None if abs(self.start) == inf else self.start
        stop = None if abs(self.stop) == inf else self.stop
        return slice(start, stop)

    def __len__(self) -> int:
        if abs(self.stop) == inf or abs(self.start) == inf:
            return inf
        return self.stop - self.start

    def __repr__(self) -> str:
        return f"[{self.start} to {self.stop - 1}]"


class CubeSlice:
    def __init__(self, on: bool, xslice: NooiceSlice, yslice: NooiceSlice, zslice: NooiceSlice):
        self.on = on
        self.x = xslice
        self.y = yslice
        self.z = zslice

    @property
    def off(self):
        return not self.on

    def __eq__(self, other: "CubeSlice"):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def intersect(self, other: "CubeSlice") -> "CubeSlice | None":
        x_inter = self.x & other.x
        if x_inter != NooiceSlice(0, 0):
            y_inter = self.y & other.y
            if y_inter != NooiceSlice(0, 0):
                z_inter = self.z & other.z
                if z_inter != NooiceSlice(0, 0):
                    return CubeSlice(True, x_inter, y_inter, z_inter)
        return None

    def __and__(self, other: "CubeSlice") -> "CubeSlice | None":
        return self.intersect(other)

    def adjacent(self, other: "CubeSlice") -> bool:
        return self._adjacent_x(other) or self._adjacent_y(other) or self._adjacent_z(other)

    def _adjacent_x(self, other: "CubeSlice") -> bool:
        return self.x.adjacent(other.x) and self.y == other.y and self.z == other.z

    def _adjacent_y(self, other: "CubeSlice") -> bool:
        return self.y.adjacent(other.y) and self.x == other.x and self.z == other.z

    def _adjacent_z(self, other: "CubeSlice") -> bool:
        return self.z.adjacent(other.z) and self.x == other.x and self.y == other.y

    def combine(self, other: "CubeSlice") -> "CubeSlice":
        if self._adjacent_x(other):
            return CubeSlice(True, self.x.combine(other.x), self.y, self.z)
        if self._adjacent_y(other):
            return CubeSlice(True, self.x, self.y.combine(other.y), self.z)
        if self._adjacent_z(other):
            return CubeSlice(True, self.x, self.y, self.z.combine(other.z))

    def __abs__(self) -> int:
        return len(self.x) * len(self.y) * len(self.z)

    def disjoint(self, other) -> bool:
        return self.intersect(other) is None

    def points_iter(self) -> Generator:
        yield from product(
            range(self.x.start, self.x.stop),
            range(self.y.start, self.y.stop),
            range(self.z.start, self.z.stop),
        )

    def __contains__(self, pt: tuple[int, int, int]) -> bool:
        x, y, z = pt
        return x in self.x and y in self.y and z in self.z

    def __lt__(self, other: "CubeSlice") -> bool:
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other: "CubeSlice") -> bool:
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __repr__(self) -> str:
        on_off = "on" if self.on else "off"
        x, y, z = self.x, self.y, self.z
        return f"{on_off} x={x.start}..{x.stop},y={y.start}..{y.stop},z={z.start}..{z.stop}"


def parse_input(s: str) -> list[CubeSlice]:
    cube_slices = re.findall(r"(on|off) x=(-*\d+)..(-*\d+),y=(-*\d+)..(-*\d+),z=(-*\d+)..(-*\d+)", s)
    slices = []
    for on_off, xmin, xmax, ymin, ymax, zmin, zmax in cube_slices:
        x = NooiceSlice(int(xmin), int(xmax) + 1)
        y = NooiceSlice(int(ymin), int(ymax) + 1)
        z = NooiceSlice(int(zmin), int(zmax) + 1)
        slc = CubeSlice(on_off == "on", x, y, z)
        slices.append(slc)
    return slices


def part_b(s: str) -> int:
    """
    Examples:
    >>> cubes = parse_input(test_strings[0])
    >>> cube = Cube()
    >>> cube.add_slice(cubes[0])
    >>> expected_points = read_points_str(expected_points_strs[0])
    >>> assert set(cube.points_iter()) == expected_points
    >>> cube.add_slice(cubes[1])
    >>> expected_points |= read_points_str(expected_points_strs[1])
    >>> assert set(cube.points_iter()) == expected_points
    >>> cube.add_slice(cubes[2])
    >>> expected_points -= read_points_str(expected_points_strs[2])
    >>> assert set(cube.points_iter()) == expected_points
    >>> cube.add_slice(cubes[3])
    >>> expected_points |= set([(10, 10, 10)])
    >>> assert set(cube.points_iter()) == expected_points
    """
    slices = parse_input(s)
    cube = Cube()
    for i, cube_slice in enumerate(slices):
        cube.add_slice(cube_slice)
        # print(f'Now on cube slice {i} out of {len(slices)}. The cube slice is {"on" if cube_slice.on else "off"}.')

    return abs(cube)


class Cube:
    def __init__(self):
        self.__slices: list[CubeSlice] = []

    def get_slices(self) -> list[CubeSlice]:
        return self.__slices

    def set_slices(self, new_slices):
        self.__slices = new_slices

    def add_slice(self, new_slice: CubeSlice):
        intersecting_partitioned_slices = [pslice for pslice in self.__slices if not pslice.disjoint(new_slice)]
        for pslice in intersecting_partitioned_slices:
            self.__slices.remove(pslice)

        if new_slice.off:
            self.__slices.extend(
                flatten(
                    merge_adjacent_cubes(list(generate_all_products(pslice, new_slice)))
                    for pslice in intersecting_partitioned_slices
                )
            )
        else:
            self.__slices.extend(self.partition_slices([new_slice] + intersecting_partitioned_slices))

    def partition_slices(self, cube_slices: list[CubeSlice]) -> list[CubeSlice]:
        new_slices = deepcopy(cube_slices)
        partitioned_slices = []
        while len(new_slices) > 0:
            new_slice = new_slices.pop()
            all_disjoint = True

            for pslice in partitioned_slices:
                if not pslice.disjoint(new_slice):
                    all_disjoint = False
                    if new_slice <= pslice:
                        break
                    partitioned_slices.remove(pslice)
                    new_slices.extend(merge_adjacent_cubes(list(generate_all_products(pslice, new_slice))))
                    break

            if all_disjoint:
                partitioned_slices.append(new_slice)

        return partitioned_slices

    def points_iter(self) -> Generator:
        for cube_slice in self.get_slices():
            yield from cube_slice.points_iter()

    def intersections_size(self):
        inters = []
        for a in self.__slices:
            for b in self.__slices:
                inter = a.intersect(b)
                if inter is not None:
                    inters.append(inter)
        return inters

    def __abs__(self):
        return sum(abs(cube_slice) for cube_slice in self.get_slices())

    def __repr__(self) -> str:
        ret_val = ""
        for slc in self.__slices:
            ret_val += f"{slc}\n"
        return ret_val


def generate_all_products(cube1: CubeSlice, cube2: CubeSlice) -> Generator:
    """Partition the cubes into a refinement of their intersection.

    cube1 is assumed to be on and cube2 is assumed to be either on/off.

    Examples:
    >>> # Disjoint cubes
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1))
    >>> cube2 = CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(2, 3), NooiceSlice(2, 3))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> assert cube1 in cube_products
    >>> assert cube2 in cube_products
    >>> assert len(cube_products) == 2
    >>> # Disjoint cubes "touching" on a corner
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1))
    >>> cube2 = CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(1, 2))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> assert cube1 in cube_products
    >>> assert cube2 in cube_products
    >>> assert len(list(cube_products)) == 2
    >>> # Two adjacent (still disjoint) cubes
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1))
    >>> cube2 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(1, 2))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> assert cube1 in cube_products
    >>> assert cube2 in cube_products
    >>> assert len(cube_products) == 2
    >>> # Two identical cubes
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1))
    >>> cube_products = list(generate_all_products(cube1, cube1))
    >>> assert cube1 in cube_products
    >>> assert len(cube_products) == 1
    >>> # Intersecting cubes with two identical axes
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 2))
    >>> cube2 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(1, 3))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(2, 3)) in cube_products
    >>> assert len(cube_products) == 3
    >>> # Intersecting cubes with one identical axis
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 2), NooiceSlice(0, 2))
    >>> cube2 = CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 3), NooiceSlice(1, 3))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(2, 3), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(2, 3), NooiceSlice(2, 3)) in cube_products
    >>> assert len(cube_products) == 7
    >>> # Intersecting cubes with no identical axes
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 2), NooiceSlice(0, 2), NooiceSlice(0, 2))
    >>> cube2 = CubeSlice(True, NooiceSlice(1, 3), NooiceSlice(1, 3), NooiceSlice(1, 3))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> # First cube pieces
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(0, 1)) in cube_products
    >>> # Intersection
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(1, 2)) in cube_products
    >>> # Second cube pieces
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(2, 3), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(2, 3), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(1, 2), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(1, 2), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(2, 3), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(2, 3), NooiceSlice(2, 3)) in cube_products
    >>> assert len(cube_products) == 15
    >>> # Intersecting cubes with no identical axes and one cube is off
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 2), NooiceSlice(0, 2), NooiceSlice(0, 2))
    >>> cube2 = CubeSlice(False, NooiceSlice(1, 3), NooiceSlice(1, 3), NooiceSlice(1, 3))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> # First cube pieces
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(0, 1)) in cube_products
    >>> assert len(cube_products) == 7
    >>> # Turn off cube
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 2), NooiceSlice(0, 2), NooiceSlice(0, 2))
    >>> cube2 = CubeSlice(False, NooiceSlice(0, 2), NooiceSlice(0, 2), NooiceSlice(0, 2))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> assert len(cube_products) == 0
    >>> # Turn off cube (bigger)
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 2), NooiceSlice(0, 2), NooiceSlice(0, 2))
    >>> cube2 = CubeSlice(False, NooiceSlice(-1, 3), NooiceSlice(-1, 3), NooiceSlice(-1, 3))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> assert len(cube_products) == 0
    >>> # Turn off cube (smaller)
    >>> cube1 = CubeSlice(True, NooiceSlice(0, 3), NooiceSlice(0, 3), NooiceSlice(0, 3))
    >>> cube2 = CubeSlice(False, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(1, 2))
    >>> cube_products = list(generate_all_products(cube1, cube2))
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(1, 2), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(2, 3), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(2, 3), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(2, 3), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(0, 1), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(1, 2)) not in cube_products  # Intersection
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(1, 2), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(2, 3), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(2, 3), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(1, 2), NooiceSlice(2, 3), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(0, 1), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(0, 1), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(0, 1), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(1, 2), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(1, 2), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(1, 2), NooiceSlice(2, 3)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(2, 3), NooiceSlice(0, 1)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(2, 3), NooiceSlice(1, 2)) in cube_products
    >>> assert CubeSlice(True, NooiceSlice(2, 3), NooiceSlice(2, 3), NooiceSlice(2, 3)) in cube_products
    >>> assert len(cube_products) == 26
    """
    # If we order the 4 points involved in each axis, we can get three regions in the space between the 4 points
    xs = sorted({cube1.x.start, cube1.x.stop, cube2.x.start, cube2.x.stop})
    ys = sorted({cube1.y.start, cube1.y.stop, cube2.y.start, cube2.y.stop})
    zs = sorted({cube1.z.start, cube1.z.stop, cube2.z.start, cube2.z.stop})
    # These produce the starts and ends for the three regions
    xs_pairs = pairwise(xs)
    ys_pairs = pairwise(ys)
    zs_pairs = pairwise(zs)
    # By taking a product of each of these regions, we produce up to 27 possible cube regions
    for (xs_new, xe_new), (ys_new, ye_new), (zs_new, ze_new) in product(xs_pairs, ys_pairs, zs_pairs):
        # Some of the cubes are extra and need to be filtered out
        # The extra cubes can be detected by taking a corner point and testing if it belongs to one of the previous cubes
        if (
            (xs_new, ys_new, zs_new) in cube1
            and not (cube2.off and (xs_new, ys_new, zs_new) in cube2)
            or cube2.on
            and (xs_new, ys_new, zs_new) in cube2
        ):
            yield CubeSlice(
                True,
                NooiceSlice(xs_new, xe_new),
                NooiceSlice(ys_new, ye_new),
                NooiceSlice(zs_new, ze_new),
            )


@apply_until_fixed
def merge_adjacent_cubes(cubes: list[CubeSlice]) -> list[CubeSlice]:
    """
    Examples:
    >>> cubes = merge_adjacent_cubes(
    ...     [
    ...         CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 1)),
    ...         CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(1, 2)),
    ...         CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(2, 3)),
    ...         CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(3, 4)),
    ...     ]
    ... )
    >>> assert cubes == [CubeSlice(True, NooiceSlice(0, 1), NooiceSlice(0, 1), NooiceSlice(0, 4))]
    >>> assert merge_adjacent_cubes([]) == []
    """
    if len(cubes) == 1:
        return cubes

    merged_cubes = []
    already_merged = []
    for cube1, cube2 in combinations(cubes, 2):
        if cube1 in already_merged or cube2 in already_merged:
            continue
        if cube1.adjacent(cube2):
            already_merged.extend([cube1, cube2])
            merged_cubes.append(cube1.combine(cube2))

    merged_cubes += [cube for cube in cubes if cube not in already_merged]
    return merged_cubes


test_strings = [
    """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""",
    """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""",
    """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""",
]


expected_points_strs = [
    """10,10,10
10,10,11
10,10,12
10,11,10
10,11,11
10,11,12
10,12,10
10,12,11
10,12,12
11,10,10
11,10,11
11,10,12
11,11,10
11,11,11
11,11,12
11,12,10
11,12,11
11,12,12
12,10,10
12,10,11
12,10,12
12,11,10
12,11,11
12,11,12
12,12,10
12,12,11
12,12,12""",
    """11,11,13
11,12,13
11,13,11
11,13,12
11,13,13
12,11,13
12,12,13
12,13,11
12,13,12
12,13,13
13,11,11
13,11,12
13,11,13
13,12,11
13,12,12
13,12,13
13,13,11
13,13,12
13,13,13""",
    """10,10,10
10,10,11
10,11,10
10,11,11
11,10,10
11,10,11
11,11,10
11,11,11""",
]


def read_points_str(s: str):
    lines = [line.split(",") for line in s.split("\n")]
    return {(int(x), int(y), int(z)) for x, y, z in lines}


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)
