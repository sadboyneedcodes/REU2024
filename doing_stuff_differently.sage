import csv
import ast
import sage.all as sage
import logging

# Set up logging
logging.basicConfig(filename='knots_processing.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def process_csv_chunk(input_file, output_file, start_row, chunk_size):
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header

        # Skip to the start row
        for _ in range(start_row):
            next(reader)
        
        with open(output_file, 'a', newline='') as outfile:
            writer = csv.writer(outfile)
            if start_row == 0:
                writer.writerow(header)  # Write the header only for the first chunk

            for i, row in enumerate(reader):
                if i >= chunk_size:
                    break
                if row[1]:  # Check if the Seifert matrix is not empty
                    try:
                        seifert_matrix = sage.matrix(sage.SR, ast.literal_eval(row[1]))
                        det_seifert_matrix = seifert_matrix.det()
                        row[2] = str(det_seifert_matrix)
                    except Exception as e:
                        logging.error(f"Error processing row {start_row + i + 1}: {e}")
                        row[2] = 'Error'

                writer.writerow(row)  # Write the updated row to the new CSV file

def process_csv_in_chunks(input_file, output_file, chunk_size):
    start_row = 0
    while True:
        logging.info(f"Processing rows {start_row} to {start_row + chunk_size - 1}")
        process_csv_chunk(input_file, output_file, start_row, chunk_size)
        start_row += chunk_size

        if start_row % 100 == 0:
            print(f"Processed {start_row} rows...")

        with open(input_file, 'r') as f:
            total_rows = sum(1 for _ in f)

        if start_row >= total_rows:
            break
        
input_file = 'our_data.csv'
output_file = 'our_data_updated.csv'
chunk_size = 100  # Adjust chunk size as needed

# Initialize the output file (create new or truncate existing)
with open(output_file, 'w') as f:
    pass

process_csv_in_chunks(input_file, output_file, chunk_size)

print("Processing completed. Updated CSV file has been saved as 'knots_updated.csv'")