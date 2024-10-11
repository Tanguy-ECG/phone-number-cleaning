import pandas as pd

from utils import extract_digits_with_limit_length, format_to_desired_pattern_for_mobile_number, correct_number

# Ask the user to enter the column names and provide the file path
col_phones = input(
    "Enter column names with phone numbers to clean (separated by commas): "
)

file = input(
    "Enter the file with path: "
).replace("\\", "/")

# Get columns in a list with the right format
col_phones = list(map(str.strip, col_phones.split(",")))

# Import the file
df = pd.read_csv(file, na_values = "None")

# Clean phone numbers
cleaned_columns = df[col_phones].applymap(
    lambda x: extract_digits_with_limit_length(format_to_desired_pattern_for_mobile_number(x)) if correct_number(format_to_desired_pattern_for_mobile_number(x)) else ""
)

# Copy the original DataFrame
cleaned_df = df.copy()

# Update original DataFrame with cleaned phone numbers
for col in col_phones:
    cleaned_df[col] = cleaned_columns[col].astype(str)

cleaned_df['phone'] = cleaned_df[col_phones].apply(lambda row: next((item for item in row if item), ''), axis=1)

# Count the number of valid phone numbers
nb_valid_phone_number = (cleaned_df['phone'] != "").sum()

# Calculate the percentage of valid phone numbers
percentage_valid = (nb_valid_phone_number / df.shape[0]) * 100

# Print the number of valid phone numbers and the percentage
print(
    f"Number of valid phone numbers: {nb_valid_phone_number} ({percentage_valid:.2f}%)"
)

# get only valid number phone
get_only_valid_number = input(
    "Do you want to keep only valid number phone ? (y/n)"
).lower() in ["y", "yes", "oui", "o"]

if get_only_valid_number:
    cleaned_df = cleaned_df.drop(col_phones, axis = 1)
    cleaned_df = cleaned_df.query("phone != ''")

# get only valid number phone
remove_doublons = input(
    "Do you want to remove doublons ? (y/n)"
).lower() in ["y", "yes", "oui", "o"]

if remove_doublons:
    cleaned_df = cleaned_df.drop_duplicates(["phone"])

# Export the cleaned DataFrame to a new CSV file
output_file_path = "/".join(file.split("/")[:-1]) + "/" + file.split("/")[-1].split(".")[0] + "_cleaned.csv"

if cleaned_df.shape[0] == df.shape[0] or get_only_valid_number: 
    print("Successful cleaning!")
else:
    print("ERROR")

cleaned_df.applymap(lambda x: str(x).replace(";", "") if not pd.isna(x) else x).to_csv(output_file_path, index=False, sep=";")
print("Cleaned file saved at: " + "/".join(file.split("/")[:-1]))
