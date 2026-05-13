def main():
    blueCosts = [1, 1, 1]
    greenCosts = [3, 5, 7]
    redCosts = [4, 6, 4]

    def recurse(i: int, purchases: list, cost: int) -> list:
        if i == 3:
            return cost, purchases

        if not purchases:
            return min(
                recurse(i + 1, purchases + ["b"], cost + blueCosts[i]),
                recurse(i + 1, purchases + ["g"], cost + greenCosts[i]),
                recurse(i + 1, purchases + ["r"], cost + redCosts[i]),
                key=lambda x: x[0],
            )

        if purchases[-1] == "b":
            return min(
                recurse(i + 1, purchases + ["g"], cost + greenCosts[i]),
                recurse(i + 1, purchases + ["r"], cost + redCosts[i]),
                key=lambda x: x[0],
            )
        elif purchases[-1] == "g":
            return min(
                recurse(i + 1, purchases + ["b"], cost + blueCosts[i]),
                recurse(i + 1, purchases + ["r"], cost + redCosts[i]),
                key=lambda x: x[0],
            )
        else:
            return min(
                recurse(i + 1, purchases + ["b"], cost + blueCosts[i]),
                recurse(i + 1, purchases + ["g"], cost + greenCosts[i]),
                key=lambda x: x[0],
            )

    print(recurse(0, [], 0))


main()
