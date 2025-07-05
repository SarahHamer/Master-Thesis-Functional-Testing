import pandas as pd
from collections import defaultdict

# Define input and output file paths
csv_path = 'EDIH Catalogue_v3.csv'  # Replace with your actual file path
output_path = 'EDIH_Country_Grouped.txt'

# Load the data
df = pd.read_csv(csv_path)

# Dictionary to collect country-wise EDIH lists
country_edih_map = defaultdict(list)

# Populate the dictionary with country: [EDIH names]
for _, row in df.iterrows():
    country = row.get("Country", "Unknown Country")
    edih_name = row.get("EDIH Name", "Unnamed EDIH")
    country_edih_map[country].append(edih_name)

# Write the results into a txt file
with open(output_path, "w", encoding="utf-8") as f:
    for country, edih_list in sorted(country_edih_map.items()):
        edih_list_str = ", ".join(edih_list)
        sentence = f"The EDIHs located in {country} are {edih_list_str}.\n\n"
        f.write(sentence)
