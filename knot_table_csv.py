#knot table

import pandas as pd
import ast

# Read the CSV data into a DataFrame
df = pd.read_csv("/home/cawilson1/REU2024/REU2024-2/knot_info_PD&Det_13_Crossings.csv", sep=';')

# Function to parse key and value
data_dict = {}
for index, row in df.iterrows():
    key = f"{row[0]}"
    value_str = row[1].replace(';', ',')
    value_list = ast.literal_eval(value_str)
    data_dict[key] = value_list

# Create the dictionary
#data_dict = {parse_key_value(row)[0]: parse_key_value(row)[1] for index, row in df.iterrows()}
# Write the dictionary to a text file
with open("knot_table.txt", "w") as file:
    for key in data_dict:
        file.write(f"'{key}' : {data_dict[key]} ,\n")

print("Data has been written to knot_table.txt")