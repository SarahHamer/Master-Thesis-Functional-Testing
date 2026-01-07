import pandas as pd
from collections import defaultdict

# Define input and output file paths
csv_path = 'EDIH Catalogue_v3.csv'  # Replace with your actual file path
output_path = 'EDIH_Sectors_Grouped.txt'

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

def parse_sector_engagement(sector_string, edih_name):
    # Parse formatted sector string and return a list of (sector, edih_name, engagement_description)
    results = []
    if pd.isna(sector_string):
        return results
    items = sector_string.split(",")
    for item in items:
        parts = item.strip().rsplit(" - ", 1)
        if len(parts) == 2:
            sector, value = parts
            try:
                value_int = int(value)
                engagement = engagement_map.get(value_int, "unknown involvement")
                results.append((sector.strip(), edih_name, engagement))
            except ValueError:
                continue
    return results

# Dictionary to collect sector-wise EDIH lists
sector_edih_map = defaultdict(list)

# Iterate through each row and populate the dictionary
for _, row in df.iterrows():
    edih_name = row.get("EDIH Name", "Unnamed EDIH")
    sector_entries = parse_sector_engagement(row.get("Formatted sectors", ""), edih_name)
    for sector, name, engagement in sector_entries:
        sector_edih_map[sector].append(f"{name} with {engagement}")

# Write the results into a txt file
with open(output_path, "w", encoding="utf-8") as f:
    for sector, edih_list in sorted(sector_edih_map.items()):
        sentence = f"The EDIHs that are active in the sector {sector} are {', '.join(edih_list)}.\n\n"
        f.write(sentence)
