import pandas as pd
import numpy as np

np.random.seed(42)

n_customers = 1000

data = {
    "customer_id": range(1, n_customers + 1),
    "gender": np.random.choice(["Male", "Female"], n_customers),
    "age": np.random.randint(18, 80, n_customers),
    "senior_citizen": np.random.choice([0, 1], n_customers, p=[0.85, 0.15]),
    "contract_type": np.random.choice(
        ["Month-to-month", "One year", "Two year"],
        n_customers,
        p=[0.55, 0.25, 0.20]
    ),
    "tenure_months": np.random.randint(1, 72, n_customers),
    "internet_service": np.random.choice(
        ["Fiber optic", "DSL", "No"],
        n_customers,
        p=[0.45, 0.40, 0.15]
    ),
    "monthly_usage_gb": np.round(np.random.uniform(5, 300, n_customers), 1),
    "support_calls": np.random.poisson(1.5, n_customers),
    "monthly_charges": np.round(np.random.uniform(20, 120, n_customers), 2),
}

df = pd.DataFrame(data)

# Total charges como función del tenure
df["total_charges"] = np.round(
    df["monthly_charges"] * df["tenure_months"], 2
)

# Generación de churn con lógica de negocio
churn_probability = (
    0.4 * (df["contract_type"] == "Month-to-month").astype(int) +
    0.3 * (df["support_calls"] > 3).astype(int) +
    0.2 * (df["tenure_months"] < 12).astype(int)
)

df["churn"] = np.where(
    churn_probability + np.random.rand(n_customers) > 0.8,
    "Yes",
    "No"
)

# Guardar Excel
df.to_excel("customers_churn.xlsx", sheet_name="customers_data", index=False)

print("Archivo 'customers_churn.xlsx' creado correctamente.")