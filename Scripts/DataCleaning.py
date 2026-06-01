# =========================
# DATA CLEANING - CUSTOMER CHURN

import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)

# ---------- 1. CARGA DE DATOS ----------
df = pd.read_excel(
    "/workspaces/Data_Analysis/customers_churn.xlsx",
    sheet_name="customers_data"
)

# ---------- 2. INSPECCIÓN INICIAL ----------
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
df.head()
df.info()

# ---------- 3. CALIDAD DE DATOS ----------
# Valores nulos
print("\nValores nulos por columna:")
print(df.isna().sum())

# Duplicados
print("\nDuplicados:")
print(df.duplicated().sum())
df = df.drop_duplicates()

# ---------- 4. LIMPIEZA DE TEXTO ----------
categorical_cols = [
    "gender",
    "contract_type",
    "internet_service",
    "churn"
]

for col in categorical_cols:
    df[col] = df[col].astype(str).str.strip()

# ---------- 5. CONVERSIÓN DE TIPOS ----------
df["senior_citizen"] = df["senior_citizen"].map({0: "No", 1: "Yes"}).astype("category")
df["churn"] = df["churn"].astype("category")

for col in ["gender", "contract_type", "internet_service"]:
    df[col] = df[col].astype("category")

# ---------- 6. VALIDACIONES LÓGICAS ----------
df = df[df["age"].between(18, 90)]
df = df[df["tenure_months"] > 0]

# ---------- 7. REVISIÓN NUMÉRICA ----------
numeric_cols = [
    "age",
    "tenure_months",
    "monthly_usage_gb",
    "monthly_charges",
    "total_charges",
    "support_calls"
]

print("\nResumen estadístico:")
df[numeric_cols].describe()

# ---------- 8. FEATURE ENGINEERING ----------
df["tenure_group"] = pd.cut(
    df["tenure_months"],
    bins=[0, 12, 36, 72],
    labels=["0-12", "13-36", "37-72"]
)

# ---------- 9. CHECK FINAL ----------
df.info()
df.head()

# ---------- 10. GUARDAR DATA LIMPIA ----------
df.to_excel("customers_churn_clean.xlsx", sheet_name="customers_data", index=False)
print("\n Dataset limpio guardado en /data/processed/")