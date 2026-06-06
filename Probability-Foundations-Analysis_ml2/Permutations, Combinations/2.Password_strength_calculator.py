from math import log2, perm, comb

def password_combinations(length, charset_size, allow_repeats=True):
    """
    Calculate total number of possible passwords.
    allow_repeats=True  → each character can repeat (most real passwords)
    allow_repeats=False → no repeated characters
    """
    # your code here
    if(allow_repeats):
        return charset_size**length
    else:
       return perm(charset_size, length)
    

def bits_of_entropy(n_combinations):
    return log2(n_combinations)


configs = [
    (6,  10, True,  "6-digit PIN"),
    (8,  26, True,  "8 lowercase letters"),
    (8,  62, True,  "8 alphanumeric"),
    (12, 94, True,  "12 mixed (all printable ASCII)"),
    (4,  26, False, "4 unique letters (no repeat)"),
]

print(f"{'Config':<35} {'Combinations':>20} {'Entropy (bits)':>15}")
print("-" * 75)
for length, charset, repeats, label in configs:
    n = password_combinations(length, charset, repeats)
    bits = bits_of_entropy(n)
    print(f"{label:<35} {n:>20,} {bits:>14.1f}")