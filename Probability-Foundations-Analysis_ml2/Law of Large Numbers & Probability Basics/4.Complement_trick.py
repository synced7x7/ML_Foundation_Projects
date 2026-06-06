#A bag has 5 red, 3 blue, 2 green balls. You draw 3 balls without replacement.
from itertools import combinations

balls = ['R']*5 + ['B']*3 + ['G']*2  # ['R','R','R','R','R','B','B','B','G','G']

all_draws = list(combinations(range(10), 3))  
total = len(all_draws)

# Direct: P(at least one Red)
p_direct = sum (
    1 for draw in all_draws if any(balls[i] == 'R' for i in draw)
) / total

# Complement: P(at least one Red) = 1 - P(no Red)
p_no_red = sum(
    1 for draw in all_draws
    if all(balls[i] != 'R' for i in draw)
) / total
p_complement = 1 - p_no_red

print(f"Direct method:     {p_direct:.4f}")
print(f"Complement method: {p_complement:.4f}")
print(f"Both equal: {abs(p_direct - p_complement) < 1e-10}")
