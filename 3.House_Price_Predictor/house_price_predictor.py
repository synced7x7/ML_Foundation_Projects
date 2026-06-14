# =============================================================================
#  HOUSE PRICE PREDICTOR — End-to-End Machine Learning Project
#  Week 1 Sunday Project | AI Engineering Roadmap
#  Author  : Tasnif Emran (SyncedX)
#  Dataset : California Housing (sklearn.datasets)
#  Model   : Linear Regression (OLS + Polynomial features)
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy import stats

def load_data():
    try:
        import os
        csv_path = 'housing.csv'
        if os.path.exists(csv_path):
            print(f"  Source: {csv_path} (local fallback)")
            return pd.read_csv(csv_path)
        raise RuntimeError(
            "Could not fetch data online and no local CSV found.\n"
            "Run: python -c \"from sklearn.datasets import fetch_california_housing; "
            "fetch_california_housing(as_frame=True).frame.to_csv('california_housing_local.csv', index=False)\""
        )
       
    except Exception:
        from sklearn.datasets import fetch_california_housing
        data = fetch_california_housing(as_frame=True)
        print("  Source: sklearn.datasets.fetch_california_housing (online)")
        return data.frame

# ── Plot style ────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor':   '#FAFAF9',
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'axes.grid':        True,
    'grid.color':       '#EBEBEA',
    'grid.linewidth':   0.7,
    'font.family':      'sans-serif',
    'font.size':        11,
})

TEAL   = '#0F6E56'
CORAL  = '#993C1D'
AMBER  = '#854F0B'
BLUE   = '#185FA5'
GRAY   = '#888780'
LIGHT  = '#E1F5EE'

print("=" * 65)
print("  CALIFORNIA HOUSING — HOUSE PRICE PREDICTOR")
print("  End-to-end ML pipeline: EDA → Model → Evaluation")
print("=" * 65)


# =============================================================================
# SECTION 1 — DATA LOADING AND INITIAL EXPLORATION
# =============================================================================
print("\n[1/8] Loading data...")

df     = load_data()
TARGET = 'MedHouseVal'

print(f"\n  Shape        : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"  Target       : {TARGET} (median house value in $100k)")
print(f"  Missing vals : {df.isnull().sum().sum()}")
print(f"\n  Feature descriptions:")
feat_desc = {
    'MedInc':    'Median income in block group (tens of $1,000)',
    'HouseAge':  'Median house age in block group (years)',
    'AveRooms':  'Average number of rooms per household',
    'AveBedrms': 'Average number of bedrooms per household',
    'Population':'Block group population',
    'AveOccup':  'Average number of household members',
    'Latitude':  'Block group latitude',
    'Longitude': 'Block group longitude',
}
for feat, desc in feat_desc.items():
    print(f"    {feat:12s}: {desc}")

print(f"\n  Descriptive statistics:")
print(df.describe().round(3).to_string())


# =============================================================================
# SECTION 2 — EXPLORATORY DATA ANALYSIS
# =============================================================================
print("\n[2/8] Running EDA — generating plots/01_eda_overview.png ...")

fig = plt.figure(figsize=(18, 12))
gs  = gridspec.GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)

# ── 2a. Target distribution ──────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
ax1.hist(df[TARGET], bins=60, color=TEAL, edgecolor='white', linewidth=0.4)
ax1.axvline(df[TARGET].median(), color=CORAL, linestyle='--', linewidth=1.5,
            label=f"Median = ${df[TARGET].median()*100:.0f}k")
ax1.set_title("Target distribution — median house value", fontweight='500')
ax1.set_xlabel("Median house value ($100k)")
ax1.set_ylabel("Count")
ax1.legend()

# Data quality note on the plot
capped = (df[TARGET] == df[TARGET].max()).sum()
ax1.annotate(f"⚠ {capped:,} values capped at ${df[TARGET].max()*100:.0f}k",
             xy=(df[TARGET].max(), 0), xytext=(3.5, 1200),
             fontsize=9, color=CORAL,
             arrowprops=dict(arrowstyle='->', color=CORAL, lw=1))

# ── 2b. Log-transformed target ───────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2:])
log_target = np.log1p(df[TARGET])
ax2.hist(log_target, bins=60, color=BLUE, edgecolor='white', linewidth=0.4)
ax2.set_title("Log-transformed target — more normal", fontweight='500')
ax2.set_xlabel("log(1 + MedHouseVal)")
ax2.set_ylabel("Count")

# ── 2c. MedInc scatter (strongest predictor) ─────────────────────────────────
ax3 = fig.add_subplot(gs[1, :2])
ax3.scatter(df['MedInc'], df[TARGET], alpha=0.08, s=5, color=BLUE)
ax3.set_xlabel("Median income (tens of $1,000)")
ax3.set_ylabel("Median house value ($100k)")
ax3.set_title("MedInc vs house price (ρ = 0.69)", fontweight='500')

# ── 2d. Geographic price map ─────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 2:])
sc = ax4.scatter(df['Longitude'], df['Latitude'],
                 c=df[TARGET], cmap='RdYlGn', s=3, alpha=0.4,
                 vmin=0.5, vmax=5)
plt.colorbar(sc, ax=ax4, label='Value ($100k)', pad=0.01)
ax4.set_xlabel("Longitude")
ax4.set_ylabel("Latitude")
ax4.set_title("Geographic price distribution (California)", fontweight='500')

# ── 2e. Correlation heatmap ───────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, :2])
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, square=True, linewidths=0.4, ax=ax5,
            annot_kws={'size': 7}, cbar_kws={'shrink': .7})
ax5.set_title("Feature correlation matrix", fontweight='500')
ax5.tick_params(axis='x', rotation=45, labelsize=8)
ax5.tick_params(axis='y', rotation=0,  labelsize=8)

# ── 2f. Correlation with target ───────────────────────────────────────────────
ax6 = fig.add_subplot(gs[2, 2:])
corr_target = corr[TARGET].drop(TARGET).sort_values()
colors_bar  = [TEAL if v > 0 else CORAL for v in corr_target.values]
ax6.barh(corr_target.index, corr_target.values, color=colors_bar)
ax6.axvline(0, color=GRAY, linewidth=0.8, linestyle='--')
ax6.set_title("Feature correlations with house price", fontweight='500')
ax6.set_xlabel("Pearson correlation coefficient")
for i, (idx, val) in enumerate(corr_target.items()):
    ax6.text(val + (0.015 if val >= 0 else -0.015), i, f'{val:.2f}',
             va='center', ha='left' if val >= 0 else 'right', fontsize=9)

fig.suptitle("California Housing — Exploratory Data Analysis",
             fontsize=14, fontweight='500', y=1.01)
plt.savefig("plots/01_eda_overview.png", dpi=150, bbox_inches='tight',
            facecolor='white')
plt.close()
print("  Saved → plots/01_eda_overview.png")


# =============================================================================
# SECTION 3 — FEATURE ENGINEERING AND SELECTION
# =============================================================================
print("\n[3/8] Feature engineering and selection...")

# ── 3a. Engineer new features ─────────────────────────────────────────────────
df_eng = df.copy()
df_eng['rooms_per_person']   = df['AveRooms']   / df['AveOccup']
df_eng['bedrms_per_room']    = df['AveBedrms']  / df['AveRooms']
df_eng['pop_per_household']  = df['Population'] / df['AveOccup']
df_eng['income_x_age']       = df['MedInc']     * df['HouseAge'] / 100
df_eng['is_coastal']         = (
    ((df['Latitude']  > 36.5) & (df['Latitude']  < 38.5) & (df['Longitude'] < -121.5)) |
    ((df['Latitude']  > 33.5) & (df['Latitude']  < 35.0) & (df['Longitude'] < -119.0))
).astype(int)

engineered_feats = ['rooms_per_person', 'bedrms_per_room',
                    'pop_per_household', 'income_x_age', 'is_coastal']

print("\n  Engineered features:")
for f in engineered_feats:
    corr_val = df_eng[f].corr(df_eng[TARGET])
    print(f"    {f:22s}: corr with target = {corr_val:+.4f}")

# ── 3b. Feature selection by correlation threshold ────────────────────────────
ALL_FEATURES  = [c for c in df_eng.columns if c != TARGET]
corr_with_tgt = df_eng[ALL_FEATURES].corrwith(df_eng[TARGET]).abs()

SELECTED = corr_with_tgt[corr_with_tgt > 0.05].index.tolist()
DROPPED  = corr_with_tgt[corr_with_tgt <= 0.05].index.tolist()

print(f"\n  Features selected (|corr| > 0.05): {len(SELECTED)}")
for f in sorted(SELECTED, key=lambda x: -corr_with_tgt[x]):
    print(f"    {f:22s}: |corr| = {corr_with_tgt[f]:.4f}")

if DROPPED:
    print(f"\n  Features dropped (|corr| ≤ 0.05):  {DROPPED}")


# =============================================================================
# SECTION 4 — TRAIN / TEST SPLIT AND PREPROCESSING
# =============================================================================
print("\n[4/8] Splitting data and preprocessing...")

X = df_eng[SELECTED]
y = df_eng[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler      = StandardScaler()
X_train_sc  = scaler.fit_transform(X_train)
X_test_sc   = scaler.transform(X_test)

print(f"  Train size : {X_train.shape[0]:,}  ({X_train.shape[0]/len(X)*100:.0f}%)")
print(f"  Test size  : {X_test.shape[0]:,}   ({X_test.shape[0]/len(X)*100:.0f}%)")
print(f"  Features   : {X_train.shape[1]}")


# =============================================================================
# SECTION 5 — MODEL TRAINING
# =============================================================================
print("\n[5/8] Training models...")

# ── Model 1: Baseline (median predictor) ──────────────────────────────────────
y_baseline = np.full_like(y_test, y_train.median())

# ── Model 2: Linear Regression (OLS) ─────────────────────────────────────────
lr = LinearRegression()
lr.fit(X_train_sc, y_train)
y_pred_lr = lr.predict(X_test_sc)

# ── Model 3: Ridge Regression ─────────────────────────────────────────────────
ridge = Ridge(alpha=1.0)
ridge.fit(X_train_sc, y_train)
y_pred_ridge = ridge.predict(X_test_sc)

# ── Model 4: Polynomial (degree=2) + Ridge ────────────────────────────────────
poly_pipe = Pipeline([
    ('poly',   PolynomialFeatures(degree=2, include_bias=False)),
    ('scaler', StandardScaler()),
    ('ridge',  Ridge(alpha=10.0))
])
poly_pipe.fit(X_train, y_train)
y_pred_poly = poly_pipe.predict(X_test)

# ── Cross-validation scores ───────────────────────────────────────────────────
cv_lr    = cross_val_score(LinearRegression(),
                           X_train_sc, y_train, cv=5, scoring='r2')
cv_ridge = cross_val_score(Ridge(alpha=1.0),
                           X_train_sc, y_train, cv=5, scoring='r2')

print("\n  Cross-validation R² (5-fold):")
print(f"    Linear Regression : {cv_lr.mean():.4f}  ± {cv_lr.std():.4f}")
print(f"    Ridge (α=1.0)     : {cv_ridge.mean():.4f}  ± {cv_ridge.std():.4f}")


# =============================================================================
# SECTION 6 — EVALUATION
# =============================================================================
print("\n[6/8] Evaluating models...")

def evaluate(y_true, y_pred, name):
    r2   = r2_score(y_true, y_pred)
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    pct  = mae / y_true.mean() * 100
    return {'Model': name, 'R²': r2, 'MAE ($k)': mae*100,
            'RMSE ($k)': rmse*100, 'Error %': pct}

results = pd.DataFrame([
    evaluate(y_test, y_baseline,   "Baseline (median)"),
    evaluate(y_test, y_pred_lr,    "Linear Regression"),
    evaluate(y_test, y_pred_ridge, "Ridge (α=1.0)"),
    evaluate(y_test, y_pred_poly,  "Poly degree=2 + Ridge"),
])
results = results.set_index('Model').round(3)

print("\n  Model comparison (test set):")
print(results.to_string())

best_model_name = results['R²'].idxmax()
best_r2         = results['R²'].max()
best_mae        = results.loc[best_model_name, 'MAE ($k)']
print(f"\n  Best model : {best_model_name}")
print(f"  Best R²    : {best_r2:.4f}")
print(f"  Best MAE   : ${best_mae:,.0f}")

# ── Coefficient interpretation ─────────────────────────────────────────────────
print("\n  Linear Regression — coefficient interpretation:")
coef_df = pd.Series(lr.coef_, index=SELECTED).sort_values(key=abs, ascending=False)
for feat, coef in coef_df.items():
    direction = "↑" if coef > 0 else "↓"
    print(f"    {feat:22s}: {coef:+.4f}  {direction}")
print(f"    {'Intercept':22s}: {lr.intercept_:+.4f}")


# =============================================================================
# SECTION 7 — EVALUATION PLOTS
# =============================================================================
print("\n[7/8] Generating evaluation plots → plots/02_model_evaluation.png ...")

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle("Model Evaluation — Linear Regression on California Housing",
             fontsize=14, fontweight='500', y=1.01)

y_pred   = y_pred_lr
residuals = y_test.values - y_pred

# ── 7a. Actual vs Predicted ───────────────────────────────────────────────────
ax = axes[0, 0]
ax.scatter(y_test, y_pred, alpha=0.2, s=6, color=BLUE, label='Predictions')
lim = [min(y_test.min(), y_pred.min()) - 0.1,
       max(y_test.max(), y_pred.max()) + 0.1]
ax.plot(lim, lim, 'r--', linewidth=1.5, label='Perfect prediction')
ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel("Actual house value ($100k)")
ax.set_ylabel("Predicted house value ($100k)")
ax.set_title(f"Actual vs Predicted  (R² = {r2_score(y_test, y_pred):.3f})",
             fontweight='500')
ax.legend(fontsize=9)

# ── 7b. Residuals vs Predicted ────────────────────────────────────────────────
ax = axes[0, 1]
ax.scatter(y_pred, residuals, alpha=0.2, s=6, color=TEAL)
ax.axhline(0, color=CORAL, linestyle='--', linewidth=1.5)
ax.axhline( residuals.std(), color=GRAY, linestyle=':', linewidth=1, label='±1σ')
ax.axhline(-residuals.std(), color=GRAY, linestyle=':', linewidth=1)
ax.set_xlabel("Predicted value ($100k)")
ax.set_ylabel("Residual (actual − predicted)")
ax.set_title("Residual plot — look for patterns", fontweight='500')
ax.legend(fontsize=9)

# Pattern annotation
ax.annotate("Hard ceiling → $500k data cap",
            xy=(4.9, 1.2), xytext=(3.5, 2.5),
            fontsize=8, color=CORAL,
            arrowprops=dict(arrowstyle='->', color=CORAL, lw=1))

# ── 7c. Residual distribution ─────────────────────────────────────────────────
ax = axes[0, 2]
ax.hist(residuals, bins=60, color=TEAL, edgecolor='white', linewidth=0.3,
        density=True, label='Residuals')
xr = np.linspace(residuals.min(), residuals.max(), 200)
ax.plot(xr, stats.norm.pdf(xr, residuals.mean(), residuals.std()),
        color=CORAL, linewidth=2, label='Normal fit')
ax.axvline(0, color=GRAY, linestyle='--', linewidth=1)
ax.set_xlabel("Residual value")
ax.set_ylabel("Density")
ax.set_title("Residual distribution (should be ≈ normal)", fontweight='500')
ax.legend(fontsize=9)
skewness = stats.skew(residuals)
ax.text(0.98, 0.96, f"Skewness = {skewness:.3f}", transform=ax.transAxes,
        ha='right', va='top', fontsize=9, color=GRAY)

# ── 7d. Q-Q Plot ──────────────────────────────────────────────────────────────
ax = axes[1, 0]
(osm, osr), (slope, intercept, r) = stats.probplot(residuals, dist='norm')
ax.scatter(osm, osr, s=5, alpha=0.4, color=BLUE)
line_x = np.array([min(osm), max(osm)])
ax.plot(line_x, slope * line_x + intercept, color=CORAL, linewidth=1.5)
ax.set_xlabel("Theoretical quantiles")
ax.set_ylabel("Sample quantiles")
ax.set_title("Q-Q plot — normality of residuals", fontweight='500')
ax.text(0.05, 0.93, f"R² = {r**2:.4f}", transform=ax.transAxes, fontsize=9, color=GRAY)

# ── 7e. Feature importances ───────────────────────────────────────────────────
ax = axes[1, 1]
coef_sorted = pd.Series(lr.coef_, index=SELECTED).sort_values()
bar_colors  = [TEAL if v > 0 else CORAL for v in coef_sorted.values]
ax.barh(coef_sorted.index, coef_sorted.values, color=bar_colors)
ax.axvline(0, color=GRAY, linewidth=0.8, linestyle='--')
ax.set_xlabel("Standardised coefficient")
ax.set_title("Feature importances (Linear Regression)", fontweight='500')
ax.tick_params(axis='y', labelsize=9)
for i, (idx, val) in enumerate(coef_sorted.items()):
    ax.text(val + (0.005 if val >= 0 else -0.005), i, f'{val:.3f}',
            va='center', ha='left' if val >= 0 else 'right', fontsize=8)

# ── 7f. Model comparison bar chart ───────────────────────────────────────────
ax = axes[1, 2]
models_r2 = results['R²']
bar_c = [TEAL if i == list(models_r2.index).index(best_model_name) else GRAY
         for i in range(len(models_r2))]
bars = ax.bar(range(len(models_r2)), models_r2.values, color=bar_c,
              edgecolor='white', linewidth=0.5)
ax.set_xticks(range(len(models_r2)))
ax.set_xticklabels(models_r2.index, rotation=15, ha='right', fontsize=8)
ax.set_ylabel("Test R²")
ax.set_title("Model comparison — test R²", fontweight='500')
ax.set_ylim(0, 1.0)
for bar, val in zip(bars, models_r2.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{val:.3f}', ha='center', fontsize=9, fontweight='500')

plt.tight_layout()
plt.savefig("plots/02_model_evaluation.png", dpi=150, bbox_inches='tight',
            facecolor='white')
plt.close()
print("  Saved → plots/02_model_evaluation.png")


# ── Detailed residual analysis plot ──────────────────────────────────────────
print("\n       Generating plots/03_residual_deep_dive.png ...")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Residual Deep Dive — Diagnosing Model Limitations",
             fontsize=13, fontweight='500')

# Scale-location plot
ax = axes[0]
sqrt_abs_res = np.sqrt(np.abs(residuals))
ax.scatter(y_pred, sqrt_abs_res, alpha=0.2, s=6, color=AMBER)
z = np.polyfit(y_pred, sqrt_abs_res, 1)
p = np.poly1d(z)
xfit = np.linspace(y_pred.min(), y_pred.max(), 100)
ax.plot(xfit, p(xfit), color=CORAL, linewidth=1.5)
ax.set_xlabel("Predicted value")
ax.set_ylabel("√|Residual|")
ax.set_title("Scale-location plot\n(funnel → heteroscedasticity)", fontweight='500')

# Residuals vs MedInc
ax = axes[1]
ax.scatter(X_test['MedInc'], residuals, alpha=0.2, s=6, color=BLUE)
ax.axhline(0, color=CORAL, linestyle='--', linewidth=1)
ax.set_xlabel("Median income")
ax.set_ylabel("Residual")
ax.set_title("Residuals vs MedInc\n(pattern → non-linearity)", fontweight='500')

# Residuals vs Latitude
ax = axes[2]
ax.scatter(X_test['Latitude'], residuals, alpha=0.2, s=6, color=TEAL)
ax.axhline(0, color=CORAL, linestyle='--', linewidth=1)
ax.set_xlabel("Latitude")
ax.set_ylabel("Residual")
ax.set_title("Residuals vs Latitude\n(pattern → spatial structure missed)", fontweight='500')

plt.tight_layout()
plt.savefig("plots/03_residual_deep_dive.png", dpi=150, bbox_inches='tight',
            facecolor='white')
plt.close()
print("  Saved → plots/03_residual_deep_dive.png")


# =============================================================================
# SECTION 8 — KEY FINDINGS SUMMARY
# =============================================================================
print("\n[8/8] Summary\n")
print("=" * 65)
print("  RESULTS")
print("=" * 65)
print(results.to_string())
print()
print(f"  Best model  : {best_model_name}")
print(f"  Test R²     : {best_r2:.4f}  (explains {best_r2*100:.1f}% of price variance)")
print(f"  Test MAE    : ${best_mae:,.0f}  avg prediction error")
print(f"  Baseline R² : {results.loc['Baseline (median)', 'R²']:.4f}  (random guess)")
print()
print("  KEY FINDINGS")
print("  ─────────────────────────────────────────────────────────────")
print("  1. MedInc is the strongest predictor (corr = 0.69) — wealthier")
print("     neighbourhoods have disproportionately higher house prices.")
print()
print("  2. Geographic features (Lat, Long) encode expensive coastal")
print("     clusters (SF Bay Area, LA) not captured by other features.")
print()
print("  3. The target is capped at $500,001 (4.7% of data), causing")
print("     the model to systematically underpredict luxury properties.")
print()
print("  4. Residual plots show heteroscedasticity — error grows with")
print("     predicted price. A log-transform of the target, or a")
print("     tree-based model, would address this directly.")
print()
print("  5. Polynomial features (degree=2) improve R² by adding")
print("     interaction terms like MedInc × Latitude, capturing the")
print("     insight that income premium is larger in coastal areas.")
print()
print("  NEXT STEPS")
print("  ─────────────────────────────────────────────────────────────")
print("  • Apply log-transform to target, refit, compare residual skew")
print("  • Try Random Forest / XGBoost (Week 2) — expect R² > 0.80")
print("  • Add distance-to-coast feature (haversine formula)")
print("  • Tune Ridge alpha with GridSearchCV")
print()
print("  Plots saved to: plots/")
print("=" * 65)
