#A disease affects 1% of the population. 
#A test is 95% accurate (if you have it, 95% chance of positive; if you don't, 5% false positive rate).
#You test positive. What's the probability you actually have the disease?

import numpy as np

np.random.seed(42)
n = 100_000
prevalence = 0.01
sensitivity = 0.95
false_positive_rate = 0.05

def bayes(prevalence, sensitivity, false_positive_rate):
    return (sensitivity * prevalence) / (
        sensitivity * prevalence +
        false_positive_rate * (1 - prevalence)
    )

has_disease = np.random.random(n) < prevalence

test_positive = np.where(
    has_disease,
    np.random.random(n) < sensitivity,        
    np.random.random(n) < false_positive_rate   
)

true_positives  = np.sum(has_disease & test_positive)
false_positives = np.sum(~has_disease & test_positive)
false_negatives = np.sum(has_disease & ~test_positive)
true_negatives  = np.sum(~has_disease & ~test_positive)

print(f"Population:      {n:,}")
print(f"True disease:    {np.sum(has_disease):,}  ({np.mean(has_disease)*100:.1f}%)")
print(f"\nOf those who tested POSITIVE ({np.sum(test_positive):,} total):")
print(f"  True positives:  {true_positives:,}")
print(f"  False positives: {false_positives:,}")
print(f"  P(disease | positive) = {true_positives / np.sum(test_positive):.4f}")
print(f"\nCompare to analytical Bayes: {bayes(prevalence, sensitivity, false_positive_rate):.4f}")

