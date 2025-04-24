#!/usr/bin/env python3
import sys
import pandas as pd

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <line_number> [output_file]")
    sys.exit(1)

# Get the target line number from command line arguments (1-indexed)
try:
    target_line_number = int(sys.argv[1])
except ValueError:
    print("Line number must be an integer!")
    sys.exit(1)

# Optional output file name; if not provided, print only to console
output_file = sys.argv[2] if len(sys.argv) > 2 else None

csv_filename = "dev-eng.csv"  # Fixed CSV file name

# Read CSV file using pandas
try:
    df = pd.read_csv(csv_filename, encoding="utf-8", engine="python")
except Exception as e:
    print(f"Error reading CSV file {csv_filename}: {e}")
    sys.exit(1)

# Check if the line number is within a valid range
if target_line_number < 1 or target_line_number > len(df):
    print(f"The specified line number {target_line_number} is out of range; the CSV file has {len(df)} rows.")
    sys.exit(1)

# Use iloc to get the target row (note that pandas indexing is 0-based)
row = df.iloc[target_line_number - 1]

# Process each field individually, preserving newline characters
output_lines = []
for col in df.columns:
    cell_value = row[col]
    # If the cell is NaN or not a string type, convert it to string before printing
    output_lines.append(f"{col}:\n{cell_value}\n")

final_output = "\n".join(output_lines)

# Print the result to the console
print("Extracted row content:")
print(final_output)

# If an output file is specified, save the content to the file
if output_file:
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"Extracted row content has been saved to {output_file}")
    except Exception as e:
        print(f"Error writing to output file {output_file}: {e}")
