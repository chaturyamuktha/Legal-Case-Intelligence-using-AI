import pandas as pd

# Load your integrated CSV
df = pd.read_csv("russia_losses_integrated.csv")

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Sort by date
df = df.sort_values(by='date')

# Step 1: Forward fill numeric columns
numeric_cols = df.select_dtypes(include=['number']).columns
df[numeric_cols] = df[numeric_cols].fillna(method='ffill')

# Step 2: Backward fill remaining numeric gaps (e.g., early missing values)
df[numeric_cols] = df[numeric_cols].fillna(method='bfill')

# Step 3: Fill text columns (like 'personnel*', 'POW') with forward fill or default
text_cols = df.select_dtypes(include=['object']).columns
for col in text_cols:
    df[col] = df[col].fillna(method='ffill')
    df[col] = df[col].fillna("Unknown")  # fallback for any remaining gaps

# Step 4: Optional — flag rows that had missing values before filling
df['missing_flag'] = df.isnull().any(axis=1)

# Step 5: Save cleaned version
df.to_csv("russia_losses_cleaned.csv", index=False)