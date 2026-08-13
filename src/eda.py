"""
eda.py
------
Exploratory analysis on the cleaned Telco churn data. Generates charts into
images/ that support the findings written up in reports/business_report.md.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 120

df = pd.read_csv("data/processed/telco_clean.csv")

tenure_order = ["0-1 yr", "1-2 yr", "2-4 yr", "4-6 yr"]
df["TenureGroup"] = pd.Categorical(df["TenureGroup"], categories=tenure_order, ordered=True)

# ---------------------------------------------------------------
# 1. Churn rate by contract type
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4.5))
churn_by_contract = df.groupby("Contract")["ChurnFlag"].mean().sort_values(ascending=False) * 100
churn_by_contract.plot(kind="bar", ax=ax, color=["#d9534f", "#f0ad4e", "#5cb85c"])
ax.set_ylabel("Churn Rate (%)")
ax.set_xlabel("")
ax.set_title("Churn Rate by Contract Type")
for i, v in enumerate(churn_by_contract):
    ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("images/churn_by_contract.png")
plt.close()

# ---------------------------------------------------------------
# 2. Churn rate by tenure group
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4.5))
churn_by_tenure = df.groupby("TenureGroup", observed=True)["ChurnFlag"].mean() * 100
churn_by_tenure.plot(kind="bar", ax=ax, color="#337ab7")
ax.set_ylabel("Churn Rate (%)")
ax.set_xlabel("")
ax.set_title("Churn Rate by Tenure Group")
for i, v in enumerate(churn_by_tenure):
    ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("images/churn_by_tenure.png")
plt.close()

# ---------------------------------------------------------------
# 3. MonthlyCharges distribution: churned vs retained
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.5))
sns.kdeplot(data=df, x="MonthlyCharges", hue="Churn", fill=True, alpha=0.4, ax=ax)
ax.set_title("Monthly Charges Distribution: Churned vs Retained")
ax.set_xlabel("Monthly Charges ($)")
plt.tight_layout()
plt.savefig("images/monthly_charges_distribution.png")
plt.close()

# ---------------------------------------------------------------
# 4. Churn rate by MonthlyCharges quartile
# ---------------------------------------------------------------
df["ChargeQuartile"] = pd.qcut(df["MonthlyCharges"], 4, labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"])
fig, ax = plt.subplots(figsize=(6, 4.5))
churn_by_quartile = df.groupby("ChargeQuartile", observed=True)["ChurnFlag"].mean() * 100
churn_by_quartile.plot(kind="bar", ax=ax, color="#5bc0de")
ax.set_ylabel("Churn Rate (%)")
ax.set_xlabel("")
ax.set_title("Churn Rate by Monthly Charges Quartile")
for i, v in enumerate(churn_by_quartile):
    ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("images/churn_by_charge_quartile.png")
plt.close()

# ---------------------------------------------------------------
# 5. Contract x Tenure heatmap
# ---------------------------------------------------------------
pivot = df.pivot_table(values="ChurnFlag", index="Contract", columns="TenureGroup", aggfunc="mean", observed=True) * 100
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="Reds", cbar_kws={"label": "Churn Rate (%)"}, ax=ax)
ax.set_title("Churn Rate (%) by Contract Type x Tenure Group")
plt.tight_layout()
plt.savefig("images/churn_heatmap_contract_tenure.png")
plt.close()

# ---------------------------------------------------------------
# 6. Churn rate by demographic factors (to show they DON'T matter much)
# ---------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
churn_by_gender = df.groupby("Gender")["ChurnFlag"].mean() * 100
churn_by_gender.plot(kind="bar", ax=axes[0], color="#9b59b6")
axes[0].set_title("Churn Rate by Gender")
axes[0].set_ylabel("Churn Rate (%)")
axes[0].set_ylim(0, 50)
for i, v in enumerate(churn_by_gender):
    axes[0].text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")

churn_by_payment = df.groupby("PaymentMethod")["ChurnFlag"].mean().sort_values(ascending=False) * 100
churn_by_payment.plot(kind="bar", ax=axes[1], color="#e67e22")
axes[1].set_title("Churn Rate by Payment Method")
axes[1].set_ylabel("Churn Rate (%)")
axes[1].set_ylim(0, 50)
axes[1].tick_params(axis='x', rotation=30)
for i, v in enumerate(churn_by_payment):
    axes[1].text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")

plt.tight_layout()
plt.savefig("images/churn_by_demographics.png")
plt.close()

# ---------------------------------------------------------------
# 7. Correlation heatmap (numeric features)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.5, 4.5))
corr = df[["Age", "Tenure", "MonthlyCharges", "TotalCharges", "ChurnFlag"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
ax.set_title("Correlation Matrix (Numeric Features)")
plt.tight_layout()
plt.savefig("images/correlation_heatmap.png")
plt.close()

print("Saved 7 charts to images/")
