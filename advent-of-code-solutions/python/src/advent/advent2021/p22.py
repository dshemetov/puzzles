"""22. Reactor Reboot https://adventofcode.com/2021/day/22

The problem involves boolean operations on rectangular regions of 2D space
https://en.wikipedia.org/wiki/Boolean_operations_on_polygons
"""

import re
from copy import deepcopy
from itertools import combinations, product
from math import inf
from typing import Generator

import numpy as np
from more_itertools import flatten

from advent.tools import apply_until_fixed


def solve_a(s: str) -> int:
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
    """A class implementing the algebra of left-closed integer intervals [a, b)."""

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
        if self.stop <= other.start or other.stop <= self.start:
            return True
        return False

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
        return f"[{self.start} to {self.stop-1}]"


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
        for x, y, z in product(
            range(self.x.start, self.x.stop),
            range(self.y.start, self.y.stop),
            range(self.z.start, self.z.stop),
        ):
            yield (x, y, z)

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


def solve_b(s: str) -> int:
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
            for pt in cube_slice.points_iter():
                yield pt

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

    cube1 is assumed to be on and cube2 is assumed to be either on/off."""
    # If we order the 4 points involved in each axis, we can get three regions in the space between the 4 points
    xs = sorted(list(set([cube1.x.start, cube1.x.stop, cube2.x.start, cube2.x.stop])))
    ys = sorted(list(set([cube1.y.start, cube1.y.stop, cube2.y.start, cube2.y.stop])))
    zs = sorted(list(set([cube1.z.start, cube1.z.stop, cube2.z.start, cube2.z.stop])))
    # These produce the starts and ends for the three regions
    xs_pairs = zip(xs[:-1], xs[1:])
    ys_pairs = zip(ys[:-1], ys[1:])
    zs_pairs = zip(zs[:-1], zs[1:])
    # By taking a product of each of these regions, we produce up to 27 possible cube regions
    for (xs_new, xe_new), (ys_new, ye_new), (zs_new, ze_new) in product(xs_pairs, ys_pairs, zs_pairs):
        # Some of the cubes are extra and need to be filtered out
        # The extra cubes can be detected by taking a corner point and testing if it belongs to one of the previous cubes
        if (xs_new, ys_new, zs_new) in cube1 and not (cube2.off and (xs_new, ys_new, zs_new) in cube2):
            yield CubeSlice(
                True,
                NooiceSlice(xs_new, xe_new),
                NooiceSlice(ys_new, ye_new),
                NooiceSlice(zs_new, ze_new),
            )
        elif cube2.on and (xs_new, ys_new, zs_new) in cube2:
            yield CubeSlice(
                True,
                NooiceSlice(xs_new, xe_new),
                NooiceSlice(ys_new, ye_new),
                NooiceSlice(zs_new, ze_new),
            )


@apply_until_fixed
def merge_adjacent_cubes(cubes: list[CubeSlice]) -> list[CubeSlice]:
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
