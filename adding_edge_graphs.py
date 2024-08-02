from sage.all_cmdline import *   # import sage library
from sage.knots.link import *
from sage import *
import snappy

_sage_const_0 = Integer(0); _sage_const_1 = Integer(1)
import ast
import sage.all as sage
import pandas as pd

# Read the CSV file
df = pd.read_csv("/home/cawilson1/REU2024/REU2024-2/knot_info_inc_PD.csv", sep=';')

#returns the list of regions with no negative values.
def abs_regions(self):
    regions = self.regions()
    return [set(abs(element) for element in reg) for reg in regions]

#returns the pd_code as a set. Used supplementarily to aid in intersection and difference checks.
def cross(self):
    return [set(pd) for pd in self.pd_code()]


#returns the complement of two sets' intersection.
def complement_intersection(set1, set2):
    return set(set1).difference(set2)

#returns the length of the intersection of two sets. used primarily for the weights of the crossings, as a set is unordered.
def common_elements(lst, s):
    list_set = set(lst)
    common = list_set.intersection(s)
    return len(common)

def tait_graph(pd):
    print("Type of pd_code:", type(pd))
    print("Content of pd_code:", pd)

    # Ensure pd is a proper list
    if isinstance(pd, str):
        import ast
        try:
            pd = ast.literal_eval(pd)
        except Exception as e:
            raise ValueError(f"Error converting pd_code from string: {e}")

    if not isinstance(pd, list):
        raise ValueError("pd_code must be a list.")
    
    for sublist in pd:
        if not isinstance(sublist, list):
            raise ValueError("Each element of pd_code must be a list.")
        for item in sublist:
            if not isinstance(item, int):
                raise ValueError("Each item in pd_code must be an integer.")

    try:
        K = Knot(pd)
    except Exception as e:
        print(f"Error initializing Knot: {e}")
        return []
    K = Knot(list(pd))
    regions = abs_regions(K)
    crossings = cross(K)
    pd_code = K.pd_code()
    faces_static = {index: tuple(region) for index, region in enumerate(regions)}
    faces = {tuple(region): index for index, region in enumerate(regions)}
    edges = []
    seen = []
    for ind in range(len(faces)):
        common_list = [c for c in crossings if len(set(faces_static[ind]).intersection(c)) == 2]

        #weight_check = [p for p in pd_code for c in common_list if common_elements(p,c) == 4]

        #common_list_weights = [weight(p) for p in weight_check]

        set_diff = [complement_intersection(c, faces_static[ind]) for c in common_list]

        neighboring_regions = [
            (key, value)
            for key, value in faces_static.items()
            for s in set_diff if len(set(value).intersection(s)) == 2
        ]

        for i in range(len(neighboring_regions)):
            if neighboring_regions[i][1] not in seen:
                edges.append((faces[faces_static[ind]], neighboring_regions[i][0]))
        seen.append(faces_static[ind])
    return edges

# Initialize counter
counter = _sage_const_0 

df['edge_graph'] = None

# Apply the function to the 'incr_pd_notation' column and store the results in 'edge_graph'
nan_values = ~df['incr_pd_notation'].isna()  # Identify NaN values in 'incr_pd_notation' column
for idx, val in df.loc[nan_values, 'incr_pd_notation'].items():
    df.at[idx, 'edge_graph'] = tait_graph(val)
    counter += _sage_const_1 
    print(f"Processed {counter} knots")

# Output debug information
print("Processing completed.")

#df.loc[nan_values, 'Type'] = df[nan_values].incr_pd_notation.apply( lambda x : knot_type(x))

# Save the DataFrame to CSV
df.to_csv("/root/Desktop/REU2024/knot_info_inc_PD_with_edge_graphs.csv", sep=';', index=False)