from math import comb

def lotto_probability(your_picks, pool_size, draws):
    #your code here
    results = {}
    for k in range(min(your_picks, draws) +1 ):
        ways_correct = comb(your_picks, k)
        ways_incorrect = comb(pool_size-your_picks, draws-k)
        total_ways = comb(pool_size, draws)
        results[k] = (ways_correct*ways_incorrect)/total_ways

    return results


probs = lotto_probability(your_picks=6, pool_size=49, draws=6)
print("6/49 Lotto match probabilities:")
print(f"{'Match':<10} {'Probability':>15} {'1 in':>15}")
for k, p in sorted(probs.items()):
    odds = int(1/p) if p > 0 else float('inf')
    print(f"{k} correct  {p:>15.8f}  {'1 in ' + f'{odds:,}':>15}")

print(f"\nSanity check — all probs sum to: {sum(probs.values()):.8f}")