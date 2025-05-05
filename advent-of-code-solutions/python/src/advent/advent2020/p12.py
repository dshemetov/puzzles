import re
from dataclasses import dataclass

import numpy as np
from numpy.linalg import matrix_power, norm

origin = np.array([0, 0])
north, west = np.array([0, 1]), np.array([-1, 0])
south, east = -north, -west
turn_right = np.array([[0, 1], [-1, 0]])


@dataclass
class State:
    ship_pos: np.ndarray
    waypoint_pos: np.ndarray

    def __eq__(self, other):
        if isinstance(other, State):
            return np.allclose(self.ship_pos, other.ship_pos) and np.allclose(self.waypoint_pos, other.waypoint_pos)
        else:
            return False


def solve_a(s: str) -> tuple[np.ndarray, np.ndarray]:
    commands = parse_commands(s)
    state = (origin, -west)

    for command in commands:
        state = execute_command_a(state, command)

    return int(norm(state[0], ord=1))


def parse_commands(s: str) -> list[tuple[str, str]]:
    return re.findall(r"(.)(\d+)", s)


def execute_command_a(state: tuple[np.ndarray, np.ndarray], command: tuple[str, str]) -> np.ndarray:
    pos, directory = state
    instruction, num = command
    if instruction == "F":
        return (pos + int(num) * directory, directory)
    if instruction == "N":
        return (pos + int(num) * north, directory)
    if instruction == "S":
        return (pos - int(num) * north, directory)
    if instruction == "W":
        return (pos + int(num) * west, directory)
    if instruction == "E":
        return (pos - int(num) * west, directory)
    if instruction == "R":
        return (pos, np.linalg.matrix_power(turn_right, int(num) // 90) @ directory)
    if instruction == "L":
        return (pos, np.linalg.matrix_power(-turn_right, int(num) // 90) @ directory)


def solve_b(s: str) -> int:
    commands = parse_commands(s)
    state = State(origin, 10 * east + north)

    for command in commands:
        state = execute_command_b(state, command)

    return int(norm(state.ship_pos, ord=1))


def execute_command_b(state: State, command: tuple[str, str]) -> np.ndarray:
    s_pos, w_pos = state.ship_pos, state.waypoint_pos
    instruction, num = command
    if instruction == "F":
        return State(s_pos + int(num) * w_pos, w_pos)
    if instruction == "N":
        return State(s_pos, w_pos + int(num) * north)
    if instruction == "S":
        return State(s_pos, w_pos + int(num) * south)
    if instruction == "W":
        return State(s_pos, w_pos + int(num) * west)
    if instruction == "E":
        return State(s_pos, w_pos + int(num) * east)
    if instruction == "R":
        return State(s_pos, matrix_power(turn_right, int(num) // 90) @ w_pos)
    if instruction == "L":
        return State(s_pos, matrix_power(-turn_right, int(num) // 90) @ w_pos)


test_string = """F10
N3
F7
R90
F11"""


class Test12a:
    def test_parse_command(self):
        assert parse_commands(test_string)[0] == ("F", "10")
        assert parse_commands(test_string)[1] == ("N", "3")
        assert parse_commands(test_string)[2] == ("F", "7")
        assert parse_commands(test_string)[3] == ("R", "90")
        assert parse_commands(test_string)[4] == ("F", "11")

    def test_update_ship(self):
        state = (np.array([0, 0]), north)
        new_state = execute_command_a(state, ("F", "10"))
        expected_state = (np.array([0, 10]), north)
        np.testing.assert_equal(new_state[0], expected_state[0])
        np.testing.assert_equal(new_state[1], expected_state[1])

        state = (np.array([0, 0]), north)
        new_state = execute_command_a(state, ("N", "3"))
        expected_state = (np.array([0, 3]), north)
        np.testing.assert_equal(new_state[0], expected_state[0])
        np.testing.assert_equal(new_state[1], expected_state[1])

        state = (np.array([0, 0]), north)
        new_state = execute_command_a(state, ("R", "90"))
        expected_state = (np.array([0, 0]), -west)
        np.testing.assert_equal(new_state[0], expected_state[0])
        np.testing.assert_equal(new_state[1], expected_state[1])

        state = (np.array([0, 0]), north)
        new_state = execute_command_a(state, ("L", "450"))
        expected_state = (np.array([0, 0]), west)
        np.testing.assert_equal(new_state[0], expected_state[0])
        np.testing.assert_equal(new_state[1], expected_state[1])

    def test_solve_a(self):
        assert solve_a(test_string) == 25


class Test12b:
    def test_parse_command(self):
        assert parse_commands(test_string)[0] == ("F", "10")
        assert parse_commands(test_string)[1] == ("N", "3")
        assert parse_commands(test_string)[2] == ("F", "7")
        assert parse_commands(test_string)[3] == ("R", "90")
        assert parse_commands(test_string)[4] == ("F", "11")

    def test_update_ship(self):
        state = State(origin, 10 * east + north)
        new_state = execute_command_b(state, ("F", "10"))
        expected_state = State(100 * east + 10 * north, 10 * east + north)
        assert new_state == expected_state

        new_state = execute_command_b(new_state, ("N", "3"))
        expected_state = State(100 * east + 10 * north, 10 * east + 4 * north)
        assert new_state == expected_state

        new_state = execute_command_b(new_state, ("F", "7"))
        expected_state = State(170 * east + 38 * north, 10 * east + 4 * north)
        assert new_state == expected_state

        new_state = execute_command_b(new_state, ("R", "90"))
        expected_state = State(170 * east + 38 * north, 4 * east + 10 * south)
        assert new_state == expected_state

        new_state = execute_command_b(new_state, ("F", "11"))
        expected_state = State(214 * east + 72 * south, 4 * east + 10 * south)
        assert new_state == expected_state

    def test_execute_commands(self):
        assert solve_b(test_string) == 214 + 72
