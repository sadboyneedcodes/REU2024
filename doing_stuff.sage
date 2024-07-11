import csv
import ast
import sage.all as sage

# Read the CSV file
with open('/home/cawilson1/REU2024/REU2024-2/our_data.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Update the rows with the determinant of the Seifert matrix
i = 0
for row in rows[1000:]:  # Skip header and example row
    if row[1]:  # Check if the Seifert matrix is not empty
        try:
            seifert_matrix = sage.matrix(sage.SR, ast.literal_eval(row[1]))
            det_seifert_matrix = seifert_matrix.det()
            row[2] = str(det_seifert_matrix)
        except Exception as e:
            print(f"Error processing row {row}: {e}")
            row[2] = 'Error'
    print(i, len(seifert_matrix[0]), det_seifert_matrix)
    i += 1

# Write the updated rows back to the CSV file
with open('our_data_updated.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Updated CSV file has been saved as 'knots_updated.csv'")


