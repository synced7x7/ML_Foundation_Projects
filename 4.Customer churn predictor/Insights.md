**Dataset overview**

7,043 telecom customers, 20 raw features, 26.5% churn rate. That 26.5% is important — it means the dataset is moderately imbalanced. Not extreme enough to require SMOTE, but enough that accuracy is a useless metric (a model predicting "no churn" always would score 73.5%). Every evaluation choice you made (F1, class_weight, stratified split) was correct because of this number.

---

**EDA — figure by figure**

**Churn distribution.** 5,174 retained vs 1,869 churned. The roughly 3:1 ratio is typical of real telecom datasets and reflects why companies invest in churn modelling — even reducing churn by 2-3 percentage points represents hundreds of customers and significant revenue.

**Tenure by churn status.** The histogram reveals the single most important pattern in the entire dataset. Churned customers (red) cluster heavily in the 0-20 month range with a sharp peak in months 1-5. Retained customers (green) are more evenly distributed with a second peak at 70+ months — the loyal long-timers. This U-shape in retention tells you the company has a severe early-life problem. If a customer survives their first year, they are dramatically more likely to stay indefinitely. The business implication is clear: almost all churn prevention budget should target the first 12 months.

**Monthly charges by churn.** The boxplot shows churned customers (Churn=1) have a noticeably higher median monthly charge (~$79) compared to retained customers (~$65). The interquartile range for churned customers is also tighter and shifted upward. This means high-paying customers are disproportionately leaving — the company's most valuable customers in revenue terms are simultaneously the most at-risk. This is a serious business problem because it means churn is not just a volume issue but a revenue-per-customer issue.

**Churn rate by contract type.** The starkest bar chart in the entire EDA. Month-to-month: 42.7%. One year: 11.3%. Two year: 2.8%. This is a 15x difference between month-to-month and two-year contracts. No other single feature in the dataset comes close to this discrimination power. The practical implication is direct: converting a month-to-month customer to a one-year contract cuts their churn probability by roughly 75%. This is your single highest-ROI retention intervention.

**Churn rate by internet service.** Fiber optic: 41.9%, DSL: 19.0%, No internet: 7.4%. Fiber is supposed to be the premium product — newer, faster, more expensive — yet it churns at more than twice the rate of DSL. This counterintuitive result points almost certainly to a service quality or support problem specific to the fiber product, not a pricing or customer profile issue. Customers paying more are leaving more. This warrants investigation into fiber service outages, speed complaints, or installation experience separately from DSL.

**Churn rate by payment method.** Electronic check has the highest churn at roughly 45%. Mailed check is next at around 25%. Automatic payment methods (bank transfer auto and credit card auto) both sit around 15%. The pattern here is about customer engagement and commitment. Automatic payment requires deliberate setup — customers who do this have self-selected into a more committed relationship with the company. Electronic check payers, by contrast, actively pay each month, which gives them a natural monthly opportunity to question whether they want to continue. Autopay removes that friction and the mental "should I stay?" moment.

**Tenure density by churn.** The KDE curves are revealing. Retained customers (green, mean=38 months) have a bimodal distribution — a small early peak then a large peak at 50-70 months. Churned customers (red, mean=18 months) peak sharply near zero and decline monotonically. The mean difference of 20 months (38 vs 18) understates the real separation — the median difference is even larger because churned customers are right-skewed by the early-life spike. This confirms that tenure is not just correlated with churn but is almost mechanically determining it: the longer someone stays, the exponentially less likely they are to leave.

**Senior vs non-senior.** Senior citizens churn at 41.7% versus 23.6% for non-seniors — nearly double. Senior customers may face more difficulty navigating billing disputes, technical issues, or switching providers, yet paradoxically they are leaving more. This could indicate that seniors are being targeted by competitor offers or that the company's customer service model is not working well for this demographic. A dedicated senior support programme could be a targeted intervention.

**Churn with vs without each service.** Security, Backup, DeviceProtection, and TechSupport all show the same pattern: customers WITHOUT the service churn at roughly 40%, customers WITH it churn at roughly 15%. These services are functioning as retention anchors — they create dependency and perceived value. StreamingTV and StreamingMovies show the opposite or flat pattern — having them does not materially reduce churn. This is critical for product strategy: the "protection and support" bundle is a churn reducer; the "entertainment" bundle is not.

**Tenure × monthly charges scatter.** The red dots (churned) cluster unmistakably in the top-left quadrant — short tenure combined with high monthly charges. The bottom-right (long tenure, any charge level) is almost entirely green. This two-dimensional view confirms what the individual charts showed, but the interaction is important: high monthly charges don't cause churn on their own — they only cause churn when combined with short tenure. A loyal customer paying $100/month is not at risk; a new customer paying $100/month is extremely at risk.

**Feature correlation with churn.** Contract has the largest negative correlation (around -0.40) — negative because the label encoding maps month-to-month to a high number and two-year to a low number, so longer contract = lower churn. Tenure is also strongly negative. OnlineSecurity and TechSupport are moderately negative — confirming what the service chart showed. On the positive side, MonthlyCharges is the strongest positive correlator, followed by PaperlessBilling, SeniorCitizen, and MultipleLines. The correlation structure is internally consistent with every other chart.

---

**Model evaluation — figure by figure**

**F1 score comparison.** Random Forest wins at 0.6311 with CV mean of ~0.635 ± 0.017. XGBoost sits at 0.6145, LightGBM at 0.6157. The gap between RF and the boosting models is small but consistent across both test F1 and cross-validation F1. The CV error bars are tight for all three models — the std of ±0.015-0.02 means the ranking is stable, not a lucky test-set split. F1 scores in the 0.61-0.63 range on this dataset are realistic — published benchmarks on the same Telco dataset from Kaggle cluster around 0.60-0.65 for tree-based models without deep tuning.

**ROC curves.** All three curves are close together with RF (0.840) slightly above XGBoost (0.836) and LightGBM (0.831). The curves separate most visibly in the 0.1-0.4 false positive rate range — this is the operationally important region because in production you would typically set a low threshold to maximise recall (catch as many churners as possible) while keeping false positive rate manageable. In that range, RF maintains a visibly higher true positive rate. The area difference is small (0.009 between RF and LightGBM) but the consistency of RF winning across all metrics rules out noise.

**Precision-Recall curves.** This is arguably more important than the ROC curves for an imbalanced classification problem. The baseline (random classifier) gives the churn rate — 0.27. All three models substantially outperform it. RF achieves Average Precision of 0.648, XGBoost 0.645, LightGBM 0.632. The PR curves show that at high recall (catching most churners, say recall=0.8), precision drops to around 0.45-0.50 — meaning roughly half the customers flagged as churners would be false alarms. This is the fundamental precision-recall tradeoff for churn: you catch more real churners but also send retention offers to customers who weren't going to leave. The business cost of each false alarm (wasted retention offer) vs each missed churner (lost customer lifetime value) should determine where on this curve you operate.

**Confusion matrices.** This is where the business interpretation lives.

Random Forest: TN=819, FP=216, FN=102, TP=272. Precision=0.557, Recall=0.727.
XGBoost: TN=798, FP=237, FN=103, TP=271. Precision=0.533, Recall=0.725.
LightGBM: TN=811, FP=224, FN=108, TP=266. Precision=0.543, Recall=0.711.

The recall numbers are the most strategically important column here. RF recalls 272 out of 374 actual churners (72.7%) — it catches nearly three quarters of people who are going to leave. The 102 false negatives (FN) are customers who will churn but the model missed — these represent lost revenue the model cannot help prevent. The 216 false positives are customers who would have stayed but get flagged for a retention intervention — they receive an unnecessary offer, which costs money but doesn't harm retention.

The business question is whether 72.7% recall is good enough. For a telecom company where a churned customer represents $50-100/month of lost recurring revenue, and a retention offer might cost $10-20, the economics heavily favour high recall even at the cost of more false positives. You should consider lowering the prediction threshold from 0.5 to 0.35-0.40, which would trade some precision for higher recall — the PR curve tells you exactly what that tradeoff looks like.

**All metrics compared.** The grouped bar chart confirms that RF dominates on F1 churn and CV F1 consistently. Interestingly, accuracy is highest for RF at 0.774 — but this is partly because RF makes fewer false positives (it's more conservative about predicting churn), which benefits accuracy but slightly hurts recall. XGBoost and LightGBM both show lower accuracy but similar recall — they're slightly more aggressive about flagging potential churners.

**Why Random Forest beat the boosting models here**

This result — RF outperforming XGBoost and LightGBM — surprises most people. Three reasons explain it on this specific dataset. First, the dataset is small (5,634 training samples) and relatively low-dimensional (54 features after encoding). Boosting's advantage grows with dataset size; on small datasets RF's variance reduction via bagging is often sufficient. Second, the churn signal here is dominated by a few very strong features (contract type, tenure) that RF handles well with simple majority-vote decision boundaries. Boosting's iterative residual correction is more valuable when errors are complex and distributed. Third, the class_weight='balanced' parameter interacts differently with each algorithm — RF uses it to upsample minority examples in each tree, which is well-suited to the 3:1 imbalance here.

---

**What the numbers mean together**

Your model correctly identifies 272 of 374 churners in the test set. If the test set represents 20% of customers, the full dataset has roughly 1,869 churners. Scaling up, a deployed version of this model would flag approximately 1,360 true churners plus about 1,017 false positives per 7,043 customers monitored. If your company's average customer lifetime value is $1,200 (2 years at $50/month) and a retention offer costs $15, then successfully retaining even 30% of the 1,360 true churners flagged gives you approximately $122,000 in preserved revenue against about $35,000 in retention offer costs — a positive ROI of roughly 3.5x even at conservative retention rates.