import ast
import sage.all as sage
import pandas as pd

# Read the CSV file
df = pd.read_csv("/home/cawilson1/REU2024/REU2024-2/test.csv")

# Function to compute determinant of Seifert matrix
def compute_matrix(matrix_str):
    try:
                # Convert the matrix string into a list of lists
        matrix_list = ast.literal_eval(matrix_str)
        
        # Initialize the SageMath matrix
        seifert_matrix = sage.Matrix(matrix_list)
        
        # Calculate determinant
        determinant_seifert_matrix = seifert_matrix.det()
        
        return Integer(determinant_seifert_matrix)
    except Exception as e:
        print(f"Error processing matrix {matrix_str}: {e}")
        return None

# Initialize counter
counter = 0

# Apply the function to the 'seifert_matrix' column and store the results in 'det_seifert_matrix'
nan_values = ~df['seifert_matrix'].isna()  # Identify NaN values in 'seifert_matrix' column
for idx, val in df.loc[nan_values, 'seifert_matrix'].items():
    df.at[idx, 'det_seifert_matrix'] = compute_matrix(val)
    counter += 1
    print(f"Processed {counter} matrices")

# Output debug information
print("Processing completed.")

df.loc[nan_values, 'det_seifert_matrix'] = df[nan_values].seifert_matrix.apply( lambda x : compute_matrix(x))

# Save the DataFrame to CSV
df.to_csv("/home/cawilson1/REU2024/REU2024-2/our_data_output.csv", sep=',', index=False)