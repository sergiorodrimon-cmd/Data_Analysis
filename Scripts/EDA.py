# =========================
# EXPLORATORY DATA ANALYSIS - CUSTOMER CHURN
# =========================

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
sns.set(style="whitegrid")

# ---------- 1. CARGA DE DATOS LIMPIOS ----------
df = pd.read_excel("/workspaces/Data_Analysis/customers_churn_clean.xlsx")

# ---------- 2. VISIÓN GENERAL ----------
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
df.head()
df.describe()

# ---------- 3. VARIABLE OBJETIVO: CHURN ----------
churn_counts = df["churn"].value_counts(normalize=True) * 100
print("\nTasa de churn (%):")
print(churn_counts)

plt.figure(figsize=(6,4))
sns.countplot(data=df, x="churn", palette="Set2")
plt.title("Distribución de Churn")
plt.ylabel("Número de clientes")
plt.xlabel("Churn")
plt.show()
plt.close()

# ---------- 4. ANÁLISIS UNIVARIADO ----------
numeric_cols = [
    "age",
    "tenure_months",
    "monthly_usage_gb",
    "monthly_charges",
    "total_charges",
    "support_calls"
]

for col in numeric_cols:
    plt.figure(figsize=(6,4))
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribución de {col}")
    plt.show()
    plt.close()

categorical_cols = [
    "gender",
    "contract_type",
    "internet_service",
    "senior_citizen"
]

for col in categorical_cols:
    plt.figure(figsize=(6,4))
    sns.countplot(data=df, x=col)
    plt.title(f"Distribución de {col}")
    plt.xticks(rotation=30)
    plt.show()
    plt.close()

# ---------- 5. ANÁLISIS BIVARIADO VS CHURN ----------
# Numéricas vs churn
for col in numeric_cols:
    plt.figure(figsize=(6,4))
    sns.boxplot(data=df, x="churn", y=col)
    plt.title(f"{col} vs Churn")
    plt.show()
    plt.close()

# Categóricas vs churn
for col in categorical_cols:
    churn_rate = (
        df.groupby(col)["churn"]
        .value_counts(normalize=True)
        .rename("rate")
        .reset_index()
    )

    churn_rate = churn_rate[churn_rate["churn"] == "Yes"]

    plt.figure(figsize=(6,4))
    sns.barplot(data=churn_rate, x=col, y="rate")
    plt.title(f"Tasa de Churn por {col}")
    plt.ylabel("Churn Rate")
    plt.xticks(rotation=30)
    plt.show()
    plt.close()

# ---------- 6. SEGMENTACIÓN ----------
plt.figure(figsize=(6,4))
sns.barplot(
    data=df,
    x="tenure_group",
    y=(df["churn"] == "Yes").astype(int)
)
plt.title("Tasa de Churn por grupo de antigüedad")
plt.ylabel("Churn Rate")
plt.xlabel("Tenure Group")
plt.show()
plt.close()

# ---------- 7. CORRELACIONES ----------
corr = df[numeric_cols].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlación")
plt.show()
plt.close()

# ---------- 8. CONCLUSIONES RÁPIDAS ----------
print("""
INSIGHTS PRELIMINARES:
- El churn se concentra en contratos mensuales.
- Los clientes con menor antigüedad presentan mayor abandono.
- Mayor uso de soporte está asociado a churn.
""")