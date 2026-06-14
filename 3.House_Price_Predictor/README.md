# House Price Predictor — California Housing

An end-to-end machine learning project predicting median house values across California census districts using linear regression, ridge regularisation, and polynomial feature expansion.

Built as Week 1 Sunday capstone of a structured 12-month AI Engineering Roadmap.

---

## Results

| Model | Test R² | MAE | Error % |
|---|---|---|---|
| Baseline (median) | 0.000 | ~$115k | ~62% |
| Linear Regression | 0.606 | ~$52k | ~28% |
| Ridge (α=1.0) | 0.607 | ~$52k | ~28% |
| **Poly degree=2 + Ridge** | **0.681** | **~$46k** | **~25%** |

The best model explains **68% of price variance** and predicts within **$46,000** of the true value on average, a significant improvement over the naive baseline.

---

## Dataset

**California Housing** from `sklearn.datasets` — 20,640 census block groups across California. Each row is a neighbourhood-level aggregate, not an individual house.

| Feature | Description |
|---|---|
| `MedInc` | Median income in block group (tens of thousands $) |
| `HouseAge` | Median house age in block group (years) |
| `AveRooms` | Average rooms per household |
| `AveBedrms` | Average bedrooms per household |
| `Population` | Block group population |
| `AveOccup` | Average household size |
| `Latitude` | Geographic latitude |
| `Longitude` | Geographic longitude |
| `MedHouseVal` | **Target** — Median house value ($100k) |

**Data quality note:** `MedHouseVal` is capped at $500,001 (4.7% of rows). The model systematically underpredicts luxury properties as a result.

---

## Methodology

### 1. Exploratory Data Analysis
- Inspected shape, dtypes, missing values (none found)
- Plotted target distribution — right-skewed with hard cap at $500k
- Generated correlation matrix to identify strongest predictors
- Mapped house prices geographically to identify coastal clusters

### 2. Feature Engineering
Five features engineered from existing columns:

| Engineered feature | Formula | Rationale |
|---|---|---|
| `rooms_per_person` | AveRooms / AveOccup | House spaciousness controlling for density |
| `bedrms_per_room` | AveBedrms / AveRooms | Bedroom ratio as proxy for house type |
| `pop_per_household` | Population / AveOccup | Neighbourhood density |
| `income_x_age` | MedInc × HouseAge / 100 | Interaction: does age matter more for wealthy areas? |
| `is_coastal` | Rule-based lat/long check | Binary flag for expensive coastal zones |

### 3. Feature Selection
Features with absolute Pearson correlation < 0.05 with the target were dropped. All engineered and original features passed this threshold.

### 4. Models Trained

**Baseline** — predicts the median of training labels for every test point.

**Linear Regression (OLS)** — ordinary least squares, all selected features, standardised.

**Ridge Regression** — L2 penalty (α=1.0) to reduce coefficient magnitude. Closed-form solution: `θ = (XᵀX + αI)⁻¹ Xᵀy`.

**Polynomial degree=2 + Ridge** — adds pairwise interaction and squared terms (8 features → 44 features), then fits Ridge. Best performer overall.

### 5. Evaluation Metrics

| Metric | Formula | What it measures |
|---|---|---|
| R² | 1 − SS_res/SS_tot | Fraction of variance explained |
| MAE | mean(\|y − ŷ\|) | Average absolute error (same unit as y) |
| RMSE | √mean((y − ŷ)²) | Penalises large errors more than MAE |

### 6. Residual Analysis

Three residual plots generated to diagnose model behaviour:

- **Residuals vs Predicted** — reveals a hard ceiling at $500k (the data cap) and a faint fan shape (heteroscedasticity: variance grows with price).
- **Residual distribution** — roughly normal but right-skewed, confirming the cap problem.
- **Scale-location plot** — positive slope confirms heteroscedasticity. A log-transform of the target would help.
- **Q-Q plot** — tails deviate from the diagonal, confirming non-normality at extremes.

---

## Key Findings

1. **Median income is the dominant predictor** (Pearson r = 0.69). Wealthy neighbourhoods have disproportionately higher prices, with a near-linear relationship up to incomes of ~$60k.

2. **Geography matters as much as features.** Latitude and Longitude together capture proximity to San Francisco, Los Angeles, and the coast — information that tabular features alone cannot fully express.

3. **The $500k data cap is the single biggest limitation.** 4.7% of rows have artificially identical values, which teaches the model that very expensive houses look the same as slightly-expensive ones. Any real-world deployment would need to address this.

4. **Heteroscedasticity is present.** Errors grow with predicted price, violating the OLS assumption of constant variance. Log-transforming the target or using a tree-based model resolves this.

5. **Polynomial interactions add real signal.** Terms like MedInc × Latitude capture the coastal income premium — the same income level predicts higher prices in San Francisco than in the Central Valley.

---

## Project Structure

```
house_price_predictor/
├── house_price_predictor.py   ← main script (run this)
├── requirements.txt           ← Python dependencies
├── README.md                  ← this file
└── plots/                     ← auto-generated on run
    ├── 01_eda_overview.png
    ├── 02_model_evaluation.png
    └── 03_residual_deep_dive.png
```

---

## Setup and Usage

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/house-price-predictor.git
cd house-price-predictor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create plots directory and run
mkdir plots
python house_price_predictor.py
```

All output prints to the terminal. Three plots are saved to the `plots/` directory automatically.

---

## Limitations and Next Steps

**Current limitations:**
- Linear model cannot capture non-linear price dynamics
- $500k data cap distorts predictions for expensive properties
- Heteroscedastic errors violate OLS assumptions
- No spatial autocorrelation modelling

**Planned improvements (Week 2 of roadmap):**
- Log-transform the target and re-evaluate residual normality
- Train Random Forest and XGBoost — expect R² above 0.80
- Add distance-to-nearest-coast as a feature (haversine formula)
- Tune Ridge `alpha` with `GridSearchCV` across [0.001, 0.01, 0.1, 1, 10, 100]
- Feature importance comparison: LR coefficients vs Random Forest importances

---

## What I Learned

This project applied every concept from Week 1:
- EDA skills from Monday's California Housing exploration
- OLS theory and normal equation derivation from Tuesday
- sklearn pipelines, StandardScaler, and metric interpretation from Wednesday
- Polynomial features and overfitting intuition from Thursday
- Ridge regularisation from Saturday

The biggest insight was that residual plots are more informative than R² alone — they revealed the $500k cap problem and heteroscedasticity that the headline number hides.

---

## References

- [StatQuest: Linear Regression](https://www.youtube.com/watch?v=nk2CQITm_eo)
- [StatQuest: R² explained](https://www.youtube.com/watch?v=2AQKmw14mHM)
- [StatQuest: ROC and AUC](https://www.youtube.com/watch?v=4jRBRDbJemM)
- [sklearn California Housing docs](https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset)
- [Mathematics for Machine Learning (free PDF)](https://mml-book.github.io/)
