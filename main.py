import pandas as pd

from utils import extract_digits_with_limit_length, format_to_desired_pattern, correct_number

# Ask the user to enter the column names and provide the file path
col_phones = input(
    "Enter column names with phone numbers to clean (separated by commas): "
)

file = input(
    "Enter the file path: "
).replace("\\", "/")

# Get columns in a list with the right format
col_phones = list(map(str.strip, col_phones.split(",")))

# Import the file
df = pd.read_csv(file)

# Clean phone numbers
cleaned_columns = df[col_phones].applymap(
    lambda x: extract_digits_with_limit_length(format_to_desired_pattern(x)) if correct_number(format_to_desired_pattern(x)) else None
)

# Copy the original DataFrame
cleaned_df = df.copy()

# Update original DataFrame with cleaned phone numbers
for col in col_phones:
    cleaned_df[col] = cleaned_columns[col]

# Count the number of valid phone numbers
nb_valid_phone_number = (cleaned_df.count(axis=1) > 0).sum()

# Calculate the percentage of valid phone numbers
percentage_valid = (nb_valid_phone_number / df.shape[0]) * 100

# Print the number of valid phone numbers and the percentage
print(
    f"Number of valid phone numbers: {nb_valid_phone_number} ({percentage_valid:.2f}%)"
)

# Export the cleaned DataFrame to a new CSV file
output_file_path = "/".join(file.split("/")[:-1]) + "/" + file.split("/")[-1].split(".")[0] + "_cleaned.csv"
cleaned_df.to_csv(output_file_path, index=False)

print("Cleaned file saved at: " + "/".join(file.split("/")[:-1]))
if cleaned_df.shape[0] == df.shape[0]: 
    print("ligne finale ok")
else:
    print("ERREUR")