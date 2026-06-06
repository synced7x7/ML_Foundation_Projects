import numpy as np
import matplotlib.pyplot as plt

true_p = 0.6
flips = np.random.choice([1, 0], size=10_000, p=[true_p, 1 - true_p]) #biased

running_mean = np.cumsum(flips) / np.arange(1, len(flips) + 1)

"""--- /// Walkthrough /// ---
running_mean = (total heads so far) / (number of flips so far)
[1, 1, 2, 3] / [1, 2, 3, 4]
→ [1.0, 0.5, 0.67, 0.75] """

plt.figure(figsize=(10, 4))
plt.plot(running_mean, color='steelblue', lw=1.5, label='Estimated P(H)')
plt.axhline(true_p, color='crimson', ls='--', lw=1.5, label=f'True P(H) = {true_p}')
plt.xscale('log')
plt.xlabel('Number of flips (log scale)')
plt.ylabel('Estimated probability')
plt.title('Law of Large Numbers — biased coin')
plt.legend()
plt.tight_layout()
plt.show()