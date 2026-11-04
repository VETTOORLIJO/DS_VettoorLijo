# 🛡️ Fraud Detection System

An end-to-end machine learning project that detects fraudulent financial
transactions in real time, deployed as an interactive **Streamlit** web app.

---

## 📌 Table of Contents

1. Objective
2. Dataset Used
3. Project Structure
4. Models Used
5. Methodology
6. Key Results
7. Streamlit App
8. How to Run Locally
9. Tech Stack
10. Future Improvements
---

## 🎯 Objective

Financial fraud costs businesses and consumers billions every year. Manual
rule-based fraud checks are slow, brittle, and cannot keep up with modern
transaction volumes.

The goal of this project is to build a **machine learning classifier** that:

- Accurately distinguishes **fraudulent** from **legitimate** transactions.
- Handles the **class imbalance** typical of fraud data (fraud ≈ 30% in this
  dataset; real-world fraud is often < 1%).
- Exposes the trained model through an **interactive web application** so a
  user (e.g., a fraud analyst) can score a new transaction in seconds.

**Success criteria:**
- Maximise **Recall** (catch as many frauds as possible) without
  destroying Precision.
- Achieve a strong **F1-score** and **ROC-AUC** on a held-out test set.

---

##Dataset Used

| Attribute | Details |
|-----------|---------|
| **Name** | `FraudTransactionsDataset.csv` |
| **Rows** | 50,000 transactions |
| **Columns** | 21 (raw) → 38 (after encoding) |
| **Target** | `Fraud_Label` — `1` = fraud, `0` = legitimate |
| **Class balance** | ≈ 32.1% fraud / 67.9% legitimate |
| **Source** | `<ADD SOURCE — e.g., Kaggle / internal bank extract / synthetic generator>` |
| **Original link** | `<ADD URL — e.g., https://www.kaggle.com/datasets/...>` |
| **License** | `<ADD LICENSE — e.g., CC0 / Public Domain>` |

### Feature groups

| Group | Example columns |
|-------|-----------------|
| **Transaction info** | `Transaction_Amount`, `Transaction_Type`, `Timestamp`, `Account_Balance` |
| **Channel / device** | `Device_Type`, `Location`, `IP_Address_Flag`, `Authentication_Method` |
| **Merchant** | `Merchant_Category`, `Card_Type`, `Card_Age` |
| **Behavioural / risk** | `Daily_Transaction_Count`, `Avg_Transaction_Amount_7d`, `Failed_Transaction_Count_7d`, `Transaction_Distance`, `Risk_Score`, `Previous_Fraudulent_Activity` |
| **Derived** | `Day_of_Week`, `Hour`, `Is_Weekend` |

### Preprocessing pipeline

1. **EDA** — distribution plots, KDE, boxplots, correlation matrix.
2. **Cleaning** — no missing values or duplicates were found.
3. **Feature engineering** — `Day_of_Week` and `Hour` derived from `Timestamp`.
4. **Encoding** — one-hot encoding for all nominal categoricals
   (`drop_first=True`).
5. **Scaling** — `StandardScaler` for distance/gradient-based models.
6. **Imbalance handling** — **SMOTE** applied to the training set only
   (never to the test set).
7. **Split** — 80/20 stratified train-test split (`random_state=42`).

---

---

##  Models Used

Six classifiers were trained and compared on the same preprocessed data.
Each was chosen for a specific reason:

| # | Model | Why this model? |
| 1 | Logistic Regression	: Baseline. Fast, interpretable, and establishes the performance floor every other model must beat. 
| 2 | Ridge Classifier tuned)	:L2-regularised linear model — reduces overfitting vs. plain Logistic Regression while keeping the interpretability of a linear decision boundary. Good for many one-hot features. 
| 3 | Random Forest tuned)	:Bagged ensemble of decision trees. Captures non-linear feature interactions (e.g., *Risk_Score × Failed_Transaction_Count*) without feature scaling. Robust to outliers. 
| 4 | XGBoost(tuned)		:Gradient-boosted trees — typically the strongest off-the-shelf model for tabular fraud data. Handles imbalance well via `scale_pos_weight` and is fast on 50k rows. |
| 5 | Support Vector Machine (RBF kernel) : Strong on high-dimensional, moderately-sized datasets; finds a maximum-margin boundary that separates fraud clusters cleanly. Chosen as a high-capacity non-linear model to challenge the tree ensembles. 
| 6 | K-Nearest Neighbours(exploratory)  : Instance-based model included as a sanity check — no training cost, but slow at inference on 50k points. 

### Hyperparameter tuning

`GridSearchCV` (5-fold `StratifiedKFold`, scoring = accuracy / F1) was used
for Ridge, Random Forest, XGBoost, and SVM. Key tuned params:

- **Ridge** — `alpha ∈ {0.001 … 100}`, `solver`
- **Random Forest** — `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`
- **XGBoost** — `n_estimators`, `learning_rate`, `max_depth`
- **SVM** — `C`, `kernel`, `gamma`

### Class-imbalance strategy

- **SMOTE** (Synthetic Minority Oversampling TEchnique) on the training set only.
- `class_weight='balanced'` used on a per-model basis where SMOTE was *not*
  applied, to avoid **double-correction** (a bug worth calling out — using
  both simultaneously collapses recall).

---

## Key Results

All metrics below are on the **20% held-out test set** (10,000 transactions —
6,787 legitimate, 3,213 fraudulent), **after fixing the train/predict
feature-space mismatch** described in the notebook review.

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|:--------:|:---------:|:------:|:--------:|
| Logistic Regression | 0.7895 | 0.6704 | 0.6785 | 0.6744 |
| Ridge Classifier *(tuned)* | 0.7901 | 0.6723 | 0.6763 | 0.6743 |
| Random Forest *(tuned)* | `<fill>` | `<fill>` | `<fill>` | `<fill>` |
| XGBoost *(tuned)* | `<fill>` | `<fill>` | `<fill>` | `<fill>` |
| KNN | `<fill>` | `<fill>` | `<fill>` | `<fill>` |
| **SVM (RBF)** | **0.9513** | **0.8969** | **0.9586** | **0.9267** |

### Best Model — SVM (RBF kernel)

The **Support Vector Machine with an RBF kernel** was the clear winner:

- **Accuracy: 95.13%**
- **Precision: 89.69%** — ~90% of flagged transactions were truly fraudulent.
- **Recall: 95.86%** — it caught nearly all real frauds, which is the metric
  that matters most in fraud detection (missing a fraud is costlier than a
  false alarm).
- **F1-Score: 92.67%** — best harmonic balance of precision and recall.
- **Confusion matrix:** `[[6433, 354], [133, 3080]]` → only **133 frauds
  missed** and **354 false alarms** out of 10,000 test transactions.

**Why SVM won:** fraud patterns in this dataset appear to be **linearly
separable in a moderately high-dimensional one-hot space**, so an RBF kernel
finds a clean margin without overfitting. Tree ensembles (RF, XGB) had high
precision but collapsed on recall because SMOTE + `class_weight='balanced'`
were applied together. Logistic/Ridge underperform because they cannot model
the non-linear boundaries that the kernel trick captures.

---

##  Streamlit App


https://dsvettoorlijo.streamlit.app/

---

