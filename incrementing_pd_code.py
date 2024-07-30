
from sage.all_cmdline import *   # import sage library
import snappy

_sage_const_0 = Integer(0); _sage_const_1 = Integer(1)
import ast
import sage.all as sage
import pandas as pd

# Read the CSV file
df = pd.read_csv("/root/Desktop/REU2024/just_name.csv")
    
def knot_from_table(name):
    import snappy
    def sage_pd_code(link):
        pd = link.PD_code()
        return [[element + 1 for element in tup] for tup in pd]
    L = snappy.Link(str(name))
    snappd = sage_pd_code(L)
    return snappd

# Initialize counter
counter = _sage_const_0 

df['incr_pd_notation'] = None

# Apply the function to the 'Name' column and store the results in 'incr_pd_notation'
nan_values = ~df['Name'].isna()  # Identify NaN values in 'Name' column
for idx, val in df.loc[nan_values, 'Name'].items():
    df.at[idx, 'incr_pd_notation'] = knot_from_table(val)
    counter += _sage_const_1 
    print(f"Processed {counter} knots")

# Output debug information
print("Processing completed.")

#df.loc[nan_values, 'Type'] = df[nan_values].Name.apply( lambda x : knot_type(x))

# Save the DataFrame to CSV
df.to_csv("/root/Desktop/REU2024/knot_info_inc_PD.csv", sep=';', index=False)