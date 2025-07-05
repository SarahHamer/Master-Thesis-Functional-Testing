import pandas as pd
from collections import defaultdict

# Define input and output file paths
csv_path = 'EDIH Catalogue_v3.csv'  # Replace with your actual file path
output_path = 'EDIH_Services_Grouped.txt'

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

def parse_service_engagement(service_string, edih_name):
    """
    Parse a formatted service string and return a list of (service, edih_name, engagement_description).
    """
    results = []
    if pd.isna(service_string):
        return results
    items = service_string.split(",")
    for item in items:
        parts = item.strip().rsplit(" - ", 1)
        if len(parts) == 2:
            service, value = parts
            try:
                value_int = int(value)
                engagement = engagement_map.get(value_int, "unknown involvement")
                results.append((service.strip(), edih_name, engagement))
            except ValueError:
                continue
    return results

# Dictionary to collect service-wise EDIH lists
service_edih_map = defaultdict(list)

# Iterate through each row and populate the dictionary
for _, row in df.iterrows():
    edih_name = row.get("EDIH Name", "Unnamed EDIH")
    service_entries = parse_service_engagement(row.get("Formatted services", ""), edih_name)
    for service, name, engagement in service_entries:
        service_edih_map[service].append(f"{name} with {engagement}")

# Write the results into a txt file
with open(output_path, "w", encoding="utf-8") as f:
    for service, edih_list in sorted(service_edih_map.items()):
        sentence = f"The EDIHs that are active in the service area {service} are {', '.join(edih_list)}.\n\n"
        f.write(sentence)
