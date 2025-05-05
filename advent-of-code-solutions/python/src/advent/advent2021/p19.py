"""Beacon Scanner
https://adventofcode.com/2021/day/19

I was in flight to Tampa for this one, so this is mostly Jeff and David's code.
"""

import copy
from itertools import permutations, product
from typing import Counter

import numpy as np
from scipy.spatial.distance import cdist

# Cube rotation matrices
# https://en.wikipedia.org/wiki/Octahedral_symmetry#Rotation_matrices
cube_reflections = [np.diag(x) for x in product([-1, 1], repeat=3)]
cube_rotations = [
    reflection[list(x)]
    for x in permutations(range(3))
    for reflection in cube_reflections
    if np.linalg.det(reflection[list(x)]) > 0
]


class ScannerRotation:
    def __init__(
        self,
        x_flip: bool,
        y_flip: bool,
        z_flip: bool,
        permutation: tuple[int, int, int],
    ):
        self.x_sign = -1 if x_flip else 1
        self.y_sign = -1 if y_flip else 1
        self.z_sign = -1 if z_flip else 1
        self.permutation = permutation

    def rotate(self, points: np.ndarray) -> np.ndarray:
        new_array = np.copy(points[:, self.permutation])
        new_array[:, 0] *= self.x_sign
        new_array[:, 1] *= self.y_sign
        new_array[:, 2] *= self.z_sign
        return new_array

    def compose(self, other: "ScannerRotation") -> "ScannerRotation":
        x_flip = self.x_sign * other.x_sign == -1
        y_flip = self.y_sign * other.y_sign == -1
        z_flip = self.z_sign * other.z_sign == -1
        other_permutation = list(other.permutation)
        permutation = tuple(other_permutation[i] for i in list(self.permutation))
        return ScannerRotation(x_flip, y_flip, z_flip, permutation)


class Scanner:
    def __init__(self, scanner_number: int, list_of_points: list[list[int]]):
        self.scanner_number = scanner_number
        self.beacons = np.array(list_of_points)
        # self.dist_mat = distance_matrix(self.beacons, self.beacons)
        self.offset = np.array([0, 0, 0])

    def add_new_points(self, other: "Scanner", offset: np.ndarray, rotation: ScannerRotation):
        rot_and_trans = (rotation @ other.beacons.T).T - offset
        blist = self.beacons.tolist()
        to_include = [list(point) not in blist for point in rot_and_trans]
        self.beacons = np.append(self.beacons, rot_and_trans[to_include, :], axis=0)

    def __repr__(self):
        ret_val = f"--- scanner {self.scanner_number} ---\n"
        for i in range(self.beacons.shape[0]):
            for j in range(self.beacons.shape[1]):
                ret_val += ("," if j > 0 else "") + str(self.beacons[i, j])
            ret_val += "\n"
        return ret_val


def solve_a(s: str) -> int:
    scanners = parse_input(s)
    to_check = copy.deepcopy(scanners[0])
    to_scan = set(scanners[1:])

    while len(to_scan) > 0:
        to_scan = scan_list(to_check, to_scan)

    return f"{to_check.beacons.shape[0]}"


def parse_input(s: str):
    sensor_lines = s.split("\n")
    scanners = []
    scanner_beacons: list[list[int]] = []
    ii_scan = -1
    for sensor_line in sensor_lines:
        if "---" in sensor_line:
            ii_scan += 1
            scanner_beacons.append([])
        elif len(sensor_line.strip()) != 0:
            scanner_beacons[ii_scan].append([int(x) for x in sensor_line.split(",")])
    for scanner in scanner_beacons:
        scanners.append(Scanner(len(scanners), scanner))

    return scanners


def scan_list(target: Scanner, to_be_scanned: set[Scanner]) -> set[Scanner]:
    to_remove = set()

    for scanner in to_be_scanned:
        for rotation in cube_rotations:
            test_beacons = (rotation @ scanner.beacons.T).T
            dist_mat = np.round(cdist(test_beacons, target.beacons, "cityblock")).astype("int")
            unique_vals, counts = np.unique(dist_mat, return_counts="True")

            point_found = False

            for dval in np.unique(counts)[::-1]:
                if dval < 12:
                    break
                # check if this possible distance has 12 of the same offset
                offsets_dict = Counter()
                dist_inds = np.where(dist_mat == unique_vals[np.where(counts == dval)])
                for i in range(len(dist_inds[0])):
                    offset = tuple(test_beacons[dist_inds[0][i]] - target.beacons[dist_inds[1][i]])
                    offsets_dict[offset] += 1
                point_found = False
                for val in offsets_dict:
                    if offsets_dict[val] >= 12:
                        target.add_new_points(scanner, val, rotation)
                        scanner.offset = np.array(val)
                        to_remove |= {scanner}
                        point_found = True
                        break
                if point_found:
                    break
            if point_found:
                break

    return to_be_scanned - to_remove


def solve_b(s: str) -> int:
    scanners = parse_input(s)
    to_check = copy.deepcopy(scanners[0])
    to_scan = set(scanners[1:])

    while len(to_scan) > 0:
        to_scan = scan_list(to_check, to_scan)

    return f"{largest_distance(scanners)}"


def largest_distance(scanners):
    maxdist = -np.inf
    for ii, x in enumerate(scanners):
        for y in scanners[ii:]:
            maxdist = max(np.linalg.norm(x.offset - y.offset, ord=1), maxdist)
    return maxdist
