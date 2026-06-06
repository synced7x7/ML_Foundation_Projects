#Setup: 3 doors. Prize behind
#  1. You pick door 1.
#  Host opens a door that has no prize (never your door, never the prize door). 
#  You can switch or stay. Should you switch?

import random

def montyHall(sw:bool) -> bool:
    doors = [0 ,0 ,1]
    random.shuffle(doors)

    player_choice = 0

    host_opens = next(
        i for i in range(3)
            if i!=player_choice and doors[i]==0
    )

    if(sw):
        final_choice = next(i for i in range(3) if i!=player_choice and i!=host_opens)
    else:
        final_choice = player_choice

    return doors[final_choice] == 1

n=10000
sw_res = sum(montyHall(True) for _ in range(n))
non_sw_res =  sum(montyHall(False) for _ in range(n))

print(f"Strategy: SWITCH    → Win rate: {sw_res/n:.4f}")
print(f"Strategy: STAY  → Win rate: {non_sw_res/n:.4f}")
print(f"\nSwitching is {sw_res/non_sw_res:.2f}x better")


#Visualization

import matplotlib.pyplot as plt

n = 10000

stay_wins = 0
switch_wins = 0

stay_history = []
switch_history = []

for i in range(1, n + 1):
    stay_result = montyHall(False)
    switch_result = montyHall(True)

    stay_wins += stay_result
    switch_wins += switch_result

    stay_history.append(stay_wins / i)
    switch_history.append(switch_wins / i)


plt.figure(figsize=(10, 5))

plt.plot(stay_history, label="STAY strategy (→ 1/3)", color="steelblue", linewidth=2)
plt.plot(switch_history, label="SWITCH strategy (→ 2/3)", color="crimson", linewidth=2)
plt.xscale('log')

plt.axhline(1/3, color="steelblue", linestyle="--", alpha=0.6)
plt.axhline(2/3, color="crimson", linestyle="--", alpha=0.6)

plt.title("Monty Hall: Win Rate Convergence Over Time", fontsize=13, weight="bold")
plt.xlabel("Number of simulations")
plt.ylabel("Win rate")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()