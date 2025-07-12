import pandas as pd
import os
import math

# === CONFIGURATION ===
input_file = 'ITC_1stJun.csv'    # Replace with your CSV filename
output_dir = 'splits'            # Folder where split files will be saved
rows_per_file = 4000             # You can change this to 500, 2000, etc.

# === CREATE OUTPUT FOLDER IF NOT EXISTS ===
os.makedirs(output_dir, exist_ok=True)

# === READ THE CSV ===
df = pd.read_csv(input_file)

# === CALCULATE HOW MANY FILES TO MAKE ===
total_rows = len(df)
num_files = math.ceil(total_rows / rows_per_file)

print(f"Total rows: {total_rows}")
print(f"Splitting into {num_files} files with {rows_per_file} rows each...")

# === SPLIT & SAVE ===
for i in range(num_files):
    start = i * rows_per_file
    end = min((i + 1) * rows_per_file, total_rows)
    split_df = df.iloc[start:end]
    split_filename = os.path.join(output_dir, f'split_{i+1}.csv')
    split_df.to_csv(split_filename, index=False)
    print(f"Saved: {split_filename} [{start} to {end}]")

print("Splitting done!")
