"""
model.py
--------
Builds and evaluates two churn classifiers (Logistic Regression as an
interpretable baseline, Random Forest for a stronger comparison), then
saves metrics and a feature-importance chart.

Feature choice: CustomerID is dropped (identifier, not signal). Age and
Gender are kept in the model despite showing almost no relationship to
churn in EDA -- this is intentional: it lets the model itself confirm
(via near-zero coefficients / low importance) that they don't matter,
rather than assuming that up front.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

df = pd.read_csv("data/processed/telco_clean.csv")

features = ["Age", "Gender", "Tenure", "MonthlyCharges", "TotalCharges", "Contract", "PaymentMethod"]
X = pd.get_dummies(df[features], columns=["Gender", "Contract", "PaymentMethod"], drop_first=True)
y = df["ChurnFlag"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
num_cols = ["Age", "Tenure", "MonthlyCharges", "TotalCharges"]
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])

results = {}

# ---------------- Logistic Regression ----------------
logreg = LogisticRegression(max_iter=1000, random_state=42)
logreg.fit(X_train_scaled, y_train)
pred_lr = logreg.predict(X_test_scaled)
proba_lr = logreg.predict_proba(X_test_scaled)[:, 1]

results["Logistic Regression"] = {
    "accuracy": accuracy_score(y_test, pred_lr),
    "precision": precision_score(y_test, pred_lr),
    "recall": recall_score(y_test, pred_lr),
    "f1": f1_score(y_test, pred_lr),
    "roc_auc": roc_auc_score(y_test, proba_lr),
}

# ---------------- Random Forest ----------------
rf = RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)
proba_rf = rf.predict_proba(X_test)[:, 1]

results["Random Forest"] = {
    "accuracy": accuracy_score(y_test, pred_rf),
    "precision": precision_score(y_test, pred_rf),
    "recall": recall_score(y_test, pred_rf),
    "f1": f1_score(y_test, pred_rf),
    "roc_auc": roc_auc_score(y_test, proba_rf),
}

metrics_df = pd.DataFrame(results).T.round(4)
metrics_df.to_csv("reports/model_metrics.csv")

# ---------------- Feature importance (Random Forest) ----------------
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 5))
importances.head(10).plot(kind="barh", ax=ax, color="#337ab7")
ax.invert_yaxis()
ax.set_title("Top 10 Feature Importances (Random Forest)")
ax.set_xlabel("Importance")
plt.tight_layout()
plt.savefig("images/feature_importance.png")
plt.close()

# ---------------- Logistic regression coefficients (interpretability) ----------------
coefs = pd.Series(logreg.coef_[0], index=X.columns).sort_values()
fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#d9534f" if c > 0 else "#5cb85c" for c in coefs]
coefs.plot(kind="barh", ax=ax, color=colors)
ax.set_title("Logistic Regression Coefficients\n(red = increases churn risk, green = reduces it)")
ax.set_xlabel("Coefficient (standardized features)")
plt.tight_layout()
plt.savefig("images/logreg_coefficients.png")
plt.close()

# ---------------- Confusion matrix (Random Forest, the stronger model) ----------------
cm = confusion_matrix(y_test, pred_rf)
fig, ax = plt.subplots(figsize=(5, 4.5))
import seaborn as sns
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Predicted: No Churn", "Predicted: Churn"],
            yticklabels=["Actual: No Churn", "Actual: Churn"], ax=ax)
ax.set_title("Random Forest -- Confusion Matrix (Test Set)")
plt.tight_layout()
plt.savefig("images/confusion_matrix.png")
plt.close()

print("=== Model comparison ===")
print(metrics_df)
print("\n=== Top 10 feature importances (Random Forest) ===")
print(importances.head(10))
print("\nSaved metrics to reports/model_metrics.csv")
print("Saved charts: feature_importance.png, logreg_coefficients.png, confusion_matrix.png")
