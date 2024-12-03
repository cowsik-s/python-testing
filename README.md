
# Qualys Scorecard Filtering Script

This repository contains a Python script to filter and format data from a Qualys Scorecard CSV file. The script ensures that the 'Target Remediation Date' column is in the `MM/DD/YYYY` format and removes excluded assets based on an exclusion list.

## Prerequisites

- Python 3.x
- pandas library

You can install the required library using pip:

```bash
pip install pandas
Files
Qualys Scorecard.csv: The input CSV file containing the Qualys Scorecard data.
Exclusion_List.csv: The CSV file containing the list of assets to be excluded.
filter_scorecard.py: The Python script to filter and format the Qualys Scorecard data.
Usage
Prepare the Input Files:

Ensure that Qualys Scorecard.csv and Exclusion_List.csv are in the same directory as the script.
The Qualys Scorecard.csv should have a column named Target Remediation Date with dates in any format.
The Exclusion_List.csv should have a column named Asset with the names of assets to be excluded.
Run the Script:

Execute the script using Python:
python filter_scorecard.py
Output:

The script will generate a filtered and formatted CSV file named Filtered_Scorecard_<timestamp>.csv in the same directory.
The Target Remediation Date column in the output file will be in the MM/DD/YYYY format.
Script Details
The script performs the following steps:

Reads the Qualys Scorecard.csv file with specified encoding.
Converts the Target Remediation Date column to datetime format and identifies rows with invalid dates.
Filters rows to include only valid dates that are today or in the future.
Formats the Target Remediation Date column to MM/DD/YYYY format.
Reads the Exclusion_List.csv file.
Splits the Asset Names (seperated by Semicolon) column into individual asset names.
Removes the excluded assets from the filtered DataFrame.
Groups by the original index to combine asset names back into a single string separated by semicolons.
Merges the final DataFrame with the original DataFrame to keep all other columns.
Fills NaN values in Asset Names and Target Remediation Date columns with original values.
Ensures the Target Remediation Date column is in the correct format.
Saves the final DataFrame to a CSV file with a timestamped filename.
Notes
Ensure that the date format in the source file is consistent to avoid issues during conversion.
Update the column names in the script if they differ in your input files.
