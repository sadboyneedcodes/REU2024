#knot table

import pandas as pd
import ast

# Read the CSV data into a DataFrame
df = pd.read_csv("/home/cawilson1/REU2024/REU2024-2/knot_info_PD&Determinant.csv", sep=',')

# Function to parse key and value
data_dict = {}
for index, row in df.iterrows():
    key = tuple(map(int, row[0].split('_')))
    value_str = row[1].replace(';', ',')
    value_list = ast.literal_eval(value_str)
    data_dict[key] = value_list

# Create the dictionary
#data_dict = {parse_key_value(row)[0]: parse_key_value(row)[1] for index, row in df.iterrows()}

print(data_dict)