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

# Format the 'Target Remediation Date' column to MM/DD/YYYY format
filtered_df.loc[:, 'Target Remediation Date'] = filtered_df['Target Remediation Date'].dt.strftime('%m/%d/%Y')

# Read the exclusion list CSV file
exclusion_list = pd.read_csv('Exclusion_List.csv', encoding='latin1')

# Correct column name based on available columns in the DataFrame
column_name = 'Asset Names (seperated by Semicolon)'

# Split the 'Asset Names (separated by Semicolon)' column into individual asset names in the Qualys Scorecard
filtered_df['Asset Names'] = filtered_df[column_name].str.split('; ')

# Flatten the list of asset names in the Qualys Scorecard
filtered_df = filtered_df.explode('Asset Names')
filtered_df['Asset Names'] = filtered_df['Asset Names'].str.strip()

# Remove the excluded assets from the filtered DataFrame
final_df = filtered_df[~filtered_df['Asset Names'].isin(exclusion_list['Asset'])]

# Group by original index to combine asset names back into a single string separated by semicolons
final_df = final_df.groupby(final_df.index).agg({
    'Asset Names': lambda x: '; '.join(x),
    'Target Remediation Date': 'first'
}).reset_index()

# Merge the final DataFrame with the original DataFrame to keep all other columns
result_df = df.drop(columns=[column_name, 'Target Remediation Date']).merge(final_df, left_index=True, right_index=True, how='left')

# Fill NaN values in 'Asset Names' and 'Target Remediation Date' columns with original values
result_df['Asset Names (seperated by Semicolon)'] = result_df['Asset Names'].fillna(df[column_name])
result_df['Target Remediation Date'] = result_df['Target Remediation Date'].fillna(df['Target Remediation Date'])

# Ensure 'Target Remediation Date' column is in the correct format (MM/DD/YYYY)
result_df['Target Remediation Date'] = pd.to_datetime(result_df['Target Remediation Date'], errors='coerce').dt.strftime('%m/%d/%Y')

# Reorder columns to match original DataFrame
result_df = result_df[df.columns]

# Get the current date and time for the filename
now = datetime.now().strftime('%Y%m%d_%H%M%S')
output_filename = f'Filtered_Scorecard_{now}.csv'

# Save the final DataFrame to a CSV file
result_df.to_csv(output_filename, index=False)

print(f"Filtering complete. The output is saved in '{output_filename}'.")