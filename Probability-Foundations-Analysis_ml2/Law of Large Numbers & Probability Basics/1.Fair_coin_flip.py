import random

def flip_coin():
    return random.choice(["H" , "T"])

def simulate_fair_coin(n):
    flip = [flip_coin() for _ in range(n)]
    return float(flip.count("H") / n)

print(simulate_fair_coin(10))
print(simulate_fair_coin(10000))
print(simulate_fair_coin(100000))