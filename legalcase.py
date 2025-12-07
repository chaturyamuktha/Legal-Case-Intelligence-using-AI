import pandas as pd

# Load datasets
equip = pd.read_csv("russia_losses_equipment.csv")
equip_corr = pd.read_csv("russia_losses_equipment_correction.csv")
personnel = pd.read_csv("russia_losses_personnel.csv")

# Ensure all three have a date column in proper datetime format.
equip['date'] = pd.to_datetime(equip['date'])
equip_corr['date'] = pd.to_datetime(equip_corr['date'])
personnel['date'] = pd.to_datetime(personnel['date'])

# Merge corrections
merged = equip.merge(equip_corr, on='date', how='left', suffixes=('', '_corr'))

# Apply corrections (example for tanks, repeat for other columns)
merged['tank_corrected'] = merged['tank'] + merged['tank_corr'].fillna(0)

final = merged.merge(personnel[['date','personnel']], on='date', how='left')
final = final.sort_values('date')
final = final.ffill()  # handle missing personnel
final.to_csv("russia_losses_integrated.csv", index=False)