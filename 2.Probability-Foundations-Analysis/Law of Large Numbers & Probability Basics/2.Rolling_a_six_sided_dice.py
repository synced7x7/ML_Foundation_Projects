import numpy as np

rolls = np.random.randint(1, 7, size=100_000)

# Estimate P(even)
p_even = np.mean(rolls % 2 == 0)
print(f"P(even) ≈ {p_even:.4f}  (true: 0.5000)")

# Estimate P(greater than 4)
p_gt4 = np.mean(rolls > 4)
print(f"P(>4)   ≈ {p_gt4:.4f}  (true: 0.3333)")

# Estimate P(even OR greater than 4)
p_either = np.mean((rolls % 2 == 0) | (rolls > 4))
print(f"P(even OR >4) ≈ {p_either:.4f}  (true: 0.6667)")