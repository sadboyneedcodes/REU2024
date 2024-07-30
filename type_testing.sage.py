
from sage.all_cmdline import *   # import sage library

_sage_const_0 = Integer(0); _sage_const_1 = Integer(1)
import ast
import sage.all as sage
import pandas as pd

# Read the CSV file
df = pd.read_csv("/root/Desktop/REU2024/knotinfo (1).csv")

def parse_pd_code(pd_code_str):
    try:
        # Replace semicolons with commas and convert to list using ast.literal_eval
        pd_code_str = pd_code_str.replace(';', ',')
        pd_code = ast.literal_eval(pd_code_str)
        return pd_code
    except Exception as e:
        print(f"Error parsing pd_code {pd_code_str}: {e}")
        return None

def knot_type(pd_code_str):
    pd_code = parse_pd_code(pd_code_str)
    Z2_list = [[Integer(p) % 2 for p in c] for c in pd_code]
    typeI = [[0, 0, 1, 1], [1, 1, 0, 0]]
    typeII = [[0,1,1,0],[1,0,0,1]]
    if all(c in typeI for c in Z2_list) == True:
        return None, None
    else:
        zero_count = sum(1 for t in Z2_list if t == typeII[0])
        one_count = sum(1 for t in Z2_list if t == typeII[1])
        return zero_count, one_count
# Initialize counter
counter = _sage_const_0 

df['[0,1,1,0]'] = None
df['[1,0,0,1]'] = None

# Apply the function to the 'seifert_matrix' column and store the results in 'det_seifert_matrix'
nan_values = ~df['PD_Notation'].isna()  # Identify NaN values in 'PD Notation' column
for idx, val in df.loc[nan_values, 'PD_Notation'].items():
    zero_count, one_count = knot_type(val)
    df.at[idx, '[0,1,1,0]'] = zero_count
    df.at[idx, '[1,0,0,1]'] = one_count
    counter += _sage_const_1 
    print(f"Processed {counter} knots")

# Output debug information
print("Processing completed.")

df.loc[nan_values, 'Type'] = df[nan_values].PD_Notation.apply( lambda x : knot_type(x))

# Save the DataFrame to CSV
df.to_csv("/root/Desktop/REU2024/knot_info_with_type.csv", sep=',', index=False)