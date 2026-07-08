def  p_shared_birthday(n_people, n_days = 365) ->float:
    all_unique = 1.0

    for i in range (n):
        all_unique *= (n_days - i)/n_days

    return 1-all_unique

for n in [10, 20, 23, 30, 50, 70]:
    p = p_shared_birthday(n)
    bar = '█' * int(p * 40)
    print(f"n={n:3d}: {p:.4f}  {bar}")