"""Two approaches to drawing Hilbert curves with turtle graphics."""

import turtle


def hilbert(level: int, angle: int, step: float):
    if level == 0:
        return

    turtle.right(angle)
    hilbert(level - 1, -angle, step)

    turtle.forward(step)
    turtle.left(angle)
    hilbert(level - 1, angle, step)

    turtle.forward(step)
    hilbert(level - 1, angle, step)

    turtle.left(angle)
    turtle.forward(step)
    hilbert(level - 1, -angle, step)
    turtle.right(angle)


def main():
    level = 3
    size = 200
    turtle.penup()
    turtle.goto(-size / 2.0, size / 2.0)
    turtle.pendown()

    # For positioning turtle
    hilbert(level, -90, size / (2**level - 1))
    turtle.done()


def lsystem(axiom: str, rules: dict[str, str], generations: int) -> str:
    for _ in range(generations):
        axiom = "".join(rules.get(ch, ch) for ch in axiom)
    return axiom


def main2():
    level = 3
    size = 200
    s = lsystem("A", {"A": "+BF-AFA-FB+", "B": "-AF+BFB+FA-"}, level)
    print("".join({"A": "", "B": ""}.get(ch, ch) for ch in s))

    turtle.penup()
    turtle.goto(-size / 2.0, size / 2.0)
    turtle.pendown()
    for ch in s:
        if ch == "F":
            turtle.forward(size / (2**level))
        elif ch == "+":
            turtle.left(90)
        elif ch == "-":
            turtle.right(90)
    turtle.done()
