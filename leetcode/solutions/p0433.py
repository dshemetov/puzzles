def p433(startGene: str, endGene: str, bank: list[str]) -> int:
    """433. Minimum Genetic Mutation https://leetcode.com/problems/minimum-genetic-mutation/

    Examples
    --------
    >>> p433("AACCGGTT", "AACCGGTA", ["AACCGGTA"])
    1
    >>> p433("AACCGGTT", "AAACGGTA", ["AACCGGTA", "AACCGCTA", "AAACGGTA"])
    2
    >>> p433("AAAAACCC", "AACCCCCC", ["AAAACCCC", "AAACCCCC", "AACCCCCC"])
    3

    """

    def get_mutations(gene: str, bank: set[str]) -> set[str]:
        return {mutation for mutation in bank if sum(1 for i in range(len(mutation)) if mutation[i] != gene[i]) == 1}

    bank2 = set(bank)
    explored = set()
    unexplored = set({startGene})
    steps = 0
    while unexplored:
        new_unexplored = set()
        for gene in unexplored:
            if gene == endGene:
                return steps
            explored |= {gene}
            for mutations in get_mutations(gene, bank2):
                if mutations not in explored:
                    new_unexplored |= {mutations}
        unexplored = new_unexplored
        bank2 -= explored
        steps += 1

    return -1
