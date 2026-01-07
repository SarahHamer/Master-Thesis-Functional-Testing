import pandas as pd
from collections import defaultdict

# Define input and output file paths
csv_path = 'EDIH Catalogue_v3.csv'  # Replace with your actual file path
output_path = 'EDIH_Technologies_Grouped.txt'

# Load the data
df = pd.read_csv(csv_path)

# Engagement score mapping
engagement_map = {
    1: "very low involvement",
    2: "low involvement",
    3: "moderate involvement",
    4: "high involvement",
    5: "very high involvement"
}

def parse_technology_engagement(technology_string, edih_name):
    # Parse formatted technology string and return a list of (technology, edih_name, engagement_description)
    results = []
    if pd.isna(technology_string):
        return results
    items = technology_string.split(",")
    for item in items:
        parts = item.strip().rsplit(" - ", 1)
        if len(parts) == 2:
            technology, value = parts
            try:
                value_int = int(value)
                engagement = engagement_map.get(value_int, "unknown involvement")
                results.append((technology.strip(), edih_name, engagement))
            except ValueError:
                continue
    return results

# Dictionary to collect technology-wise EDIH lists
technology_edih_map = defaultdict(list)

# Iterate through each row and populate the dictionary
for _, row in df.iterrows():
    edih_name = row.get("EDIH Name", "Unnamed EDIH")
    technology_entries = parse_technology_engagement(row.get("Formatted technologies", ""), edih_name)
    for technology, name, engagement in technology_entries:
        technology_edih_map[technology].append(f"{name} with {engagement}")

# Write the results into a txt file
with open(output_path, "w", encoding="utf-8") as f:
    for technology, edih_list in sorted(technology_edih_map.items()):
        sentence = f"The EDIHs that are active in the technology area {technology} are {', '.join(edih_list)}.\n\n"
        f.write(sentence)
