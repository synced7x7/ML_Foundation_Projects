from collections import defaultdict

emails = [
    ("buy cheap pills now", "spam"),
    ("win free money today", "spam"),
    ("buy now get free prize", "spam"),
    ("meeting at noon tomorrow", "ham"),
    ("project deadline is friday", "ham"),
    ("can we reschedule the meeting", "ham"),
    ("free free free click now", "spam"),
    ("lunch tomorrow works for me", "ham"),
]

word_counts = {"spam": defaultdict(int), "ham": defaultdict(int)}
class_counts = {"spam": 0, "ham": 0}

for text, label in emails:
    class_counts[label] += 1
    for word in text.split():
        word_counts[label][word] += 1

vocab = set(w for text, _ in emails for w in text.split())

def word_prob(word, cls):
    total_words = sum(word_counts[cls].values())
    return (word_counts[cls][word] + 1) / (total_words + len(vocab))  

import math

def classify(message):
    words = message.split()
    total = sum(class_counts.values())
    scores = {}
    for cls in ["spam", "ham"]:
        scores[cls] = math.log(class_counts[cls] / total)
        for word in words:
            scores[cls] += math.log(word_prob(word, cls))
    return max(scores, key=scores.get), scores

tests = [
    "free money click now",
    "meeting scheduled for friday",
    "buy free pills",
    "project update tomorrow",
]
for msg in tests:
    label, scores = classify(msg)
    print(f"'{msg}' → {label}")