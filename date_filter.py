import pandas as pd
from datetime import datetime

# Read the CSV file with specified encoding
df = pd.read_csv('Qualys Scorecard.csv', encoding='latin1')

# Ensure the 'Target Remediation Date' column is in datetime format
df['Target Remediation Date'] = pd.to_datetime(df['Target Remediation Date'], errors='coerce')

# Identify rows with invalid dates
invalid_dates = df[df['Target Remediation Date'].isna()]

# If there are invalid dates, print the row numbers and a message
if not invalid_dates.empty:
    print("Target Remediation Date is wrongly updated for the below rows in the Master Sheet. Please update it and re-run.")
    for row_number in invalid_dates.index:
        print(row_number + 2)  # Adjust for zero-based indexing and header row

# Filter rows to only include valid dates that are today or in the future
today = datetime.today().date()
filtered_df = df.loc[df['Target Remediation Date'].notna() & (df['Target Remediation Date'].dt.date >= today)].copy()

# Format the 'Target Remediation Date' column to DD/MM/YYYY format
filtered_df.loc[:, 'Target Remediation Date'] = filtered_df['Target Remediation Date'].dt.strftime('%d/%m/%Y')

# Get the current date and time for the filename
now = datetime.now().strftime('%Y%m%d_%H%M%S')
output_filename = f'Filtered_Scorecard_{now}.csv'

# Save the filtered DataFrame to a CSV file
filtered_df.to_csv(output_filename, index=False)

print(f"Filtering complete. The output is saved in '{output_filename}'.")
