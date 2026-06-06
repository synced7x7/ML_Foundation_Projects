#A disease affects 1% of the population. 
#A test is 95% accurate (if you have it, 95% chance of positive; if you don't, 5% false positive rate).
#You test positive. What's the probability you actually have the disease?

p_disease = 0.01       
p_pos_given_disease = 0.95  
p_pos_given_no_disease = 0.05 

p_no_disease = 1 - p_disease
p_positive = (p_pos_given_disease * p_disease +
              p_pos_given_no_disease * p_no_disease)

#P(disease | positive)
p_disease_given_pos = (p_pos_given_disease * p_disease) / p_positive

print(f"P(positive)             = {p_positive:.4f}")
print(f"P(disease | positive)   = {p_disease_given_pos:.4f}")
# Only about 16%! The low prior dominates.