def p263(n: int) -> bool:
    """263. Ugly Number https://leetcode.com/problems/ugly-number/"""
    if n < 1:
        return False
    while n % 2 == 0:
        n //= 2
    while n % 3 == 0:
        n //= 3
    while n % 5 == 0:
        n //= 5
    return n == 1
