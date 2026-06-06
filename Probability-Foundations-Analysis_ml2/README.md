# Probability Foundations & Analysis (ML)

A simulation project that proves probability theory computationally as well as visually — Bayes theorem, combinatorics, conditional probability, and random walks verified against analytical formulas. Because the best way to trust the math is to simulate it 100,000 times.

---

## 📂 Project Structure

The project is organized into three core probability domains:

### 1. **Conditional Probability & Bayes' Theorem**

#### 1. Medical Test & Bayes' Theorem
**File:** `1.Medical_test_bayes.py`

**Problem:** A disease affects 1% of the population. A test is 95% accurate (95% sensitivity, 5% false positive rate). If you test positive, what's the probability you actually have the disease?

**Deep Insight:** This demonstrates the counterintuitive power of **Bayes' theorem**. Most people guess ~95%. The real answer shocks them:
**The answer is about 16% — not 95%. This counterintuitive result is called the base rate fallacy and it's critical in medical AI, fraud detection, and any imbalanced classification problem.**
 The calculation uses:
$$P(\text{disease|positive}) = \frac{P(\text{positive|disease}) \cdot P(\text{disease})}{P(\text{positive})}$$
This is crucial in medical diagnosis, drug testing, and fraud detection.

---

#### 2. Medical Test Simulation on Population
**File:** `2.Medical_test_simulation_on_population_bayes.py`

**Problem:** Simulate the same disease-test scenario across a population of 100,000 and verify Bayes' theorem empirically.

**Deep Insight:** This bridges the gap between **analytical probability and real-world outcomes**. By simulating:
- Which individuals actually have the disease (based on prevalence)
- Which tests return positive (accounting for sensitivity and false positive rate)
- Computing true positives vs. false positives

The simulation verifies that theoretical Bayes calculations match empirical frequency data. Key learning: rare events + imperfect tests = many false positives. Useful in epidemiology, screening programs, and understanding base rate fallacy.

---

#### 3. Monty Hall Problem: Simulation & Visualization
**File:** `3.Monty_Hall_Problem_SimxViz.py`

**Problem:** Three doors, one prize. You pick door 1. The host opens a door with no prize (not yours, not the prize). Should you switch?

**Deep Insight:** This challenges **intuitive reasoning about conditional probability**. The counterintuitive answer: **switching wins 2/3 of the time**, staying wins 1/3. Why? After you pick a door, the probability your choice has the prize is 1/3. The host's action doesn't change this; it only reveals information. Switching pivots you to the remaining unopened door, which has a 2/3 chance. The code simulates 10,000 trials and visualizes the convergence to the theoretical 2:1 ratio. Essential for understanding how **conditioning and information reveal hidden probabilities**.

---

#### 4. Naive Bayes Spam Filter
**File:** `4.Naive Bayes spam filter.py`

**Problem:** Classify emails as spam or ham using Naive Bayes probability.

**Deep Insight:** Applies **Bayes' theorem to machine learning**. The classifier:
1. Calculates word frequencies per class (spam vs. ham)
2. Computes $P(\text{word|class})$ with Laplace smoothing to avoid zero probabilities
3. Uses **independence assumption** (Naive): treats word occurrences as independent
4. Multiplies probabilities in log-space for numerical stability

The formula: 
$$P(\text{class|words}) \propto P(\text{class}) \prod_i P(\text{word}_i|\text{class})$$

Shows how Bayes' theorem scales from medical diagnosis to real-world NLP tasks.

---

### 2. **Law of Large Numbers & Probability Basics**

#### 1. Fair Coin Flip
**File:** `1.Fair_coin_flip.py`

**Problem:** Simulate coin flips at different sample sizes and observe the convergence to 50% heads.

**Deep Insight:** Demonstrates the **Law of Large Numbers (Weak Form)**. With n=10 flips, you might get 70% heads. With n=10,000, you'll be very close to 50%. This shows:
- Small samples have high variance
- Large samples converge to the true probability
- Empirical frequency → theoretical probability

This foundation underpins all simulation-based probability verification in the project.

---

#### 2. Rolling a Six-Sided Die
**File:** `2.Rolling_a_six_sided_dice.py`

**Problem:** Roll a die 100,000 times and estimate P(even), P(>4), and P(even OR >4).

**Deep Insight:** Extends coin flip to **discrete uniform distributions**. Demonstrates:
- $P(\text{even}) = \frac{1}{2}$ (outcomes: 2,4,6)
- $P(\text{>4}) = \frac{1}{3}$ (outcomes: 5,6)
- **Probability addition rule**: $P(A \cup B) = P(A) + P(B) - P(A \cap B)$

For independent events, the simulation empirically validates set theory operations on probabilities.

---

#### 3. Law of Large Numbers - Biased Coin Visualization
**File:** `3.Law_of_large_numbers_visualization_Biased_Coin_Experiment.py`

**Problem:** Flip a biased coin (P(H)=0.6) thousands of times and plot the running average convergence.

**Deep Insight:** Visually demonstrates **LLN with a biased coin**:
- Plot shows the estimated P(H) bouncing around initially
- As sample size increases (log scale), convergence to true value (0.6) tightens
- Illustrates **standard error** proportional to $1/\sqrt{n}$

This is the intuitive proof that empirical averages converge to expected values—crucial for understanding why simulations work.

---

#### 4. Complement Trick
**File:** `4.Complement_trick.py`

**Problem:** Draw 3 balls from a bag (5 red, 3 blue, 2 green) without replacement. Find P(at least one red).

**Deep Insight:** Shows the power of **complement rule**:
$$P(\text{at least one red}) = 1 - P(\text{no red})$$

Rather than enumerating all ways to get 1, 2, or 3 reds, it's simpler to count the single case of no reds. The code verifies this analytically using combinations:
- Total draws from 10 balls: $\binom{10}{3} = 120$
- Draws with no red (only 5 blue/green): $\binom{5}{3} = 10$
- P(no red) = 10/120 = 1/12
- P(at least one red) = 1 - 1/12 ≈ 0.9167

Demonstrates combinatorial counting and why complement simplifies hard problems.

---

### 3. **Permutations & Combinations**

#### 1. The Birthday Paradox
**File:** `1.The_birthday_paradox.py`

**Problem:** In a room of n people, what's the probability at least 2 share a birthday?

**Deep Insight:** Counterintuitive result: with just 23 people, there's a >50% chance of a shared birthday (despite 365 days). The formula:
$$P(\text{at least one match}) = 1 - \prod_{i=0}^{n-1} \frac{365-i}{365}$$

Key insights:
- Counts unordered pairs: $\binom{n}{2}$ grows as $n^2$
- Birthday problem has $\Theta(n^2)$ pairs to check
- Only $n$ "opportunities" to hit the same day
- With 50 people: 99.97% probability

Foundational for understanding why coincidences are common (hash collisions, calendar sharing, etc.).

---

#### 2. Password Strength Calculator
**File:** `2.Password_strength_calculator.py`

**Problem:** Calculate the number of possible passwords and entropy for different configurations.

**Deep Insight:** Connects **combinatorics to security**:
- **With repeats** (realistic): $\text{charset}^{\text{length}}$ (e.g., $26^8$ for 8 lowercase letters)
- **Without repeats**: $P(n,k) = \frac{n!}{(n-k)!}$ (e.g., $P(26,4)$ for 4 unique letters)
- **Entropy**: $\log_2(\text{combinations})$ = bits of security

Examples:
- 6-digit PIN: $10^6 = 1M$ combinations ≈ 20 bits
- 8 alphanumeric: $62^8 ≈ 218T$ combinations ≈ 48 bits
- 12 mixed ASCII: $94^{12}$ ≈ 80 bits

Shows why longer passwords with larger charsets are exponentially stronger. Informs real-world security policies.

---

#### 3. Poker Hand Probabilities
**File:** `3.Poker_hand_probabilities.py`

**Problem:** Calculate the probability of each poker hand type (straight, flush, full house, etc.).

**Deep Insight:** Applies **combination enumeration to a real game**:
- Total 5-card hands: $\binom{52}{5} = 2,598,960$
- Straight flush: 40 hands → probability ≈ 0.0015%
- Flush: 5,108 hands → probability ≈ 0.197%
- One pair: 1,098,240 hands → probability ≈ 42.3%

The code:
1. Generates all possible hands
2. Classifies each by rank patterns and suits
3. Computes empirical probabilities

Shows why pair probability dominates (most hands are pairs) and rare hands (straight flush) occur ~1 in 65,000 times. Critical for game design and risk assessment.

---

#### 4. Lotto Probability Calculator
**File:** `4.Lotto_probability_calculator.py`

**Problem:** Calculate winning probabilities for a 6/49 lottery (pick 6 numbers from 49).

**Deep Insight:** Demonstrates **hypergeometric distribution**:
$$P(k \text{ correct}) = \frac{\binom{6}{k} \binom{43}{6-k}}{\binom{49}{6}}$$

Results for 6/49:
- 6 correct (jackpot): 1 in 13.98M
- 5 correct: 1 in 54,201
- 4 correct: 1 in 1,032
- 3 correct: 1 in 57

Key insight: **Most lottery tickets match 0-3 numbers**, making jackpot extraordinarily rare. The expected value is typically negative for players (house edge), illustrating probability applications to expected utility and decision-making.

---
