import pandas as pd
import sage.graphs.graph as graph
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import ast

def decorate_and_plot_graph(edges, name):
    G = graph.Graph(edges, multiedges=True)
    plot = G.plot(layout = 'spring', dist = 0.15, iterations = 200, edge_labels=True, title = str(name))
    plot.show(figsize = 6)

def save_all_graphs_to_pdf(csv_file, output_pdf):
    # Read the CSV file
    df = pd.read_csv(csv_file, delimiter=';')
    
    # Create a PdfPages object to save all plots in a single PDF
    with PdfPages(output_pdf) as pdf:
        # Iterate through the rows of the DataFrame
        for index, row in df.iterrows():
            name = row['Name']
            edges = ast.literal_eval(row['edge_graph'])  # Convert string representation of list to list
            fig = decorate_and_plot_graph(edges, name)
            pdf.savefig(fig)  # Save the current figure into the PDF
            plt.close(fig)  # Close the figure to free up memory

# Usage
csv_file = '/root/Desktop/REU2024/knot_info_inc_PD_with_edge_graphs.csv'  # Path to your CSV file
output_pdf = '/root/Desktop/all_graphs.pdf'  # Path to the output PDF file
save_all_graphs_to_pdf(csv_file, output_pdf)