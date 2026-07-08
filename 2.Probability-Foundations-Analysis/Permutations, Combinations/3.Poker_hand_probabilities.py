from itertools import combinations
from collections import Counter

deck = [(rank, suit) for rank in range(2, 15) for suit in range(4)]

def classify_hand(hand):
    #your code here
    ranks = sorted([r for r, _ in hand], reverse=True)
    suits = [s for _ , s in hand]
    rank_counts = Counter(ranks)
    counts = sorted([rank_counts.values()], reverse= True)
    is_flush = (len(set(suits)) == 1)
    is_straight = (len(set(suits)) == 5 and ranks[0] - ranks[4] == 4)
    if is_flush and is_straight:   return "straight flush"
    if counts[0] == 4:             return "four of a kind"
    if counts[0] == 3 and counts[1] == 2: return "full house"
    if is_flush:                   return "flush"
    if is_straight:                return "straight"
    if counts[0] == 3:             return "three of a kind"
    if counts[0] == 2 and counts[1] == 2: return "two pair"
    if counts[0] == 2:             return "one pair"
    return "high card"


from collections import Counter
hand_counts = Counter()
total = 0
for hand in combinations(deck, 5):
    hand_counts[classify_hand(hand)] += 1
    total += 1

print(f"Total hands: {total:,}\n")
for hand_type in ["high card","one pair","two pair","three of a kind",
                  "straight","flush","full house","four of a kind","straight flush"]:
    count = hand_counts[hand_type]
    print(f"{hand_type:<20} {count:>8,}  ({count/total*100:.4f}%)")