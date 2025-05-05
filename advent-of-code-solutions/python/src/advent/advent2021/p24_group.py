"""Arithmetic Logic Unit
https://adventofcode.com/2021/day/24
"""

from abc import ABC, abstractmethod
from re import findall
from typing import List

from advent.tools import get_puzzle_input


class AdventProblem(ABC):
    """
    An abstraction of an advent code problem.
    """

    def __init__(self, name: str):
        """
        :param name: a name useful for logging and debugging
        """

        self.name = name

    @abstractmethod
    def solve_part1(self) -> str:
        """
        Solve the advent problem part 1.
        """

    @abstractmethod
    def solve_part2(self) -> str:
        """
        Solve the advent problem part 2.
        """


class ALU:
    def __init__(self, instructions: List):
        from string import ascii_lowercase

        self.instructions = instructions
        self.variables = dict()
        self.back_vars = {"w": "w", "x": "x", "y": "y", "z": "z"}
        self.human_legible = list(ascii_lowercase)
        self.dict_of_functions = {
            "inp": self.inp,
            "add": self.add,
            "mul": self.mul,
            "div": self.div,
            "mod": self.mod,
            "eql": self.eql,
        }

    def get_value(self, a):
        if type(a) is str:
            return self.variables[a]
        else:
            return a

    def to_str(self):
        for op, *inp in reversed(self.instructions):
            for key in self.back_vars:
                if key == inp[0]:
                    self.back_vars[key] = self.process_op(op, inp, key)

        return self.back_vars

    def get_back_var(self, a):
        if type(a) == int:
            return a
        pot = self.back_vars[a]
        if len(pot) > 1:
            return "(" + pot.strip("(").strip(")") + ")"
        else:
            return pot

    def process_op(self, op, inp, register):
        cur_str = self.back_vars[register]
        if op == "inp":
            input_variable = self.human_legible.pop(0)
            print(f"{op}, {inp}, setting {register} to {input_variable}")
            for key2 in self.back_vars:
                self.back_vars[key2] = self.back_vars[key2].replace(register, input_variable)
            return input_variable

        val = self.get_back_var(inp[1])
        if op == "mul":
            if val == 0:
                final_value = cur_str.replace(register, "0")
                self.back_vars[register] = final_value
                for key in self.back_vars:
                    self.back_vars[key] = self.back_vars[key].replace(register, final_value)
                return register
            else:
                return cur_str.replace(register, f"{register} * {val}")
        if op == "div":
            return cur_str.replace(register, f"({register} // {val})")
        if op == "add":
            return cur_str.replace(register, f"({register} + {val})")
        if op == "eql":
            return cur_str.replace(register, f"({register} == {val})")
        if op == "mod":
            return cur_str.replace(register, f"({register} % {val})")

    def execute_instructions(self, inputs: List[int]):
        try:
            for op, *inp in self.instructions:
                fn = self.dict_of_functions[op]
                if op == "inp":
                    fn(inp[0], inputs.pop(0))
                else:
                    fn(inp[0], inp[1])
            return self.variables.get("z", 1) == 0
        except ValueError:
            return False

    def inp(self, a, b):
        self.variables[a] = b

    def add(self, a, b):
        a_val = self.variables[a]
        b_val = self.get_value(b)
        self.variables[a] = a_val + b_val

    def mul(self, a, b):
        a_val = self.variables[a]
        b_val = self.get_value(b)
        self.variables[a] = a_val * b_val

    def div(self, a, b):
        a_val = self.variables[a]
        b_val = self.get_value(b)
        if b_val == 0:
            raise ValueError("b is 0")
        self.variables[a] = a_val / b_val

    def mod(self, a, b):
        a_val = self.variables[a]
        b_val = self.get_value(b)
        if b_val <= 0:
            raise ValueError("b is non-positive")
        elif a_val < 0:
            raise ValueError("a is negative")
        self.variables[a] = a_val % b_val

    def eql(self, a, b):
        a_val = self.variables[a]
        b_val = self.get_value(b)
        self.variables[a] = 1 * a_val == b_val


def parse_input(s: str):
    program_instructions = findall(r"(inp) (\w)|(add|mod|mul|eql|div) (\w) (-*\d+|\w)", s)
    program_instructions = [
        [x if x.isalpha() else int(x) for x in instruction if x != ""] for instruction in program_instructions
    ]
    # print(program_instructions)
    return program_instructions


class Day24(AdventProblem):
    def __init__(self, test: bool):
        super().__init__("ALU")
        self.ALU = ALU(get_puzzle_input(2021, 24))

        if test:
            a = ALU(parse_input("test.txt"))
            a.execute_instructions([5])
            assert a.variables["x"] == -5
            a = ALU(parse_input("test2.txt"))
            a.execute_instructions([4, 5])
            assert a.variables["z"] == 0
            a.execute_instructions([4, 12])
            assert a.variables["z"] == 1

    def solve_part1(self) -> str:
        # num = [1,3,5,7,9,2,9,9,9,9,9]
        self.ALU.to_str()
        return self.ALU.back_vars
        # int_version = 99999999999999
        # n_rums = 0
        # while int_version > 11111111111111:
        #     array_version = [int(x) for x in str(int_version)]
        #     if n_rums % 1000 == 0:
        #         print(f"{int_version}")
        #     if any([x == 0 for x in array_version]):
        #         n_rums += 1
        #         int_version -= 1
        #         continue
        #     if self.ALU.execute_instructions(array_version):
        #         return f"{int_version}"
        #     int_version -= 1
        #     n_rums += 1
        # return "ya dumb"

    def solve_part2(self) -> str:
        return f"{3}"


def solve_a(s: str) -> int:
    return 0


def solve_b(s: str) -> int:
    return 0
