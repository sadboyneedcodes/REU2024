#import csv
import ast
import sage.all as sage



import pandas as pd
import random

df = pd.read_csv("/home/cawilson1/REU2024/REU2024-2/test.csv")

nan_values = ~df['seifert_matrix'].isna()
nan_values.at[int(0)] = False


def string_to_sage_matrix(matrix_str):
    # Remove the outer square brackets and split by rows
    rows = matrix_str.strip('[]').split('], [')
    # Convert each row into a list of integers
    matrix = [list(map(int, row.split(','))) for row in rows]
    # Create a SageMath matrix from the list of lists
    return Matrix(QQ, matrix)
    
def compute_matrix(x):
    seifert_matrix = string_to_sage_matrix(x)
    determinant_seifert_matrix = seifert_matrix.det()
    return determinant_seifert_matrix

df.loc[nan_values, 'det_seifert_matrix'] = df[nan_values].seifert_matrix.apply( lambda x : compute_matrix(x))


df.to_csv("/home/cawilson1/REU2024/REU2024-2/our_data_output.csv", sep=',')








'''



# Read the CSV file
with open('/home/cawilson1/REU2024/REU2024-2/our_data.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Update the rows with the determinant of the Seifert matrix
i = 0
for row in rows[2:]:  # Skip header and example row
    if row[1]:  # Check if the Seifert matrix is not empty
        try:
            seifert_matrix = sage.matrix(sage.SR, ast.literal_eval(row[1]))
            det_seifert_matrix = seifert_matrix.det()
            row[2] = str(det_seifert_matrix)
        except Exception as e:
            print(f"Error processing row {row}: {e}")
            row[2] = 'Error'
    print(i)
    i += 1

# Write the updated rows back to the CSV file
with open('our_data_updated.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Updated CSV file has been saved as 'knots_updated.csv'")


'''