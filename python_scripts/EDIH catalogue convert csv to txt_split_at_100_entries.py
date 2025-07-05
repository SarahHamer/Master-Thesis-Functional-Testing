import pandas as pd
from tqdm import tqdm
import math

# Define input and output
csv_path = 'EDIH Catalogue_v3.csv'  # Replace with your filename
base_output_name = 'EDIH_Catalogue_part'  # Base for multiple output files
entries_per_file = 100  # Adjustable chunk size

# Load the CSV
df = pd.read_csv(csv_path)

# Mapping from numerical values to verbal descriptions
engagement_map = {
    1: "very low involvement",
    2: "low involvement",
    3: "moderate involvement",
    4: "high involvement",
    5: "very high involvement"
}

def parse_engagement_string(field):
    """Convert engagement strings into human-readable phrases."""
    if pd.isna(field):
        return ""
    items = field.split(",")
    descriptions = []
    for item in items:
        parts = item.strip().rsplit(" - ", 1)
        if len(parts) == 2:
            name, value = parts
            try:
                value_int = int(value)
                description = f"{name.strip()} ({engagement_map.get(value_int, 'unknown level')})"
                descriptions.append(description)
            except ValueError:
                continue
    return ", ".join(descriptions)

# Explanatory note to prepend
note = (
    "NOTE:\n"
    "The 'Type' field indicates whether the EDIH has received a 'Seal of Excellence', is an EDIH, or a DIH.\n"
    "- 'EDIH' means the hub is part of the funded European Digital Innovation Hub network. It is co-funded by the European Commission and Member States/Associated Countries.\n"
    "- 'Seal of Excellence' means the hub was evaluated positively in a European competitive call but is funded exclusively by national or regional resources.\n"
    "- 'DIH' means digital innovation hubs with similar activities to EDIHs but not connected to the network.\n"
    "------------------------------------------------------------\n\n"
)

# Calculate number of output files needed
num_files = math.ceil(len(df) / entries_per_file)

for file_index in range(num_files):
    start_idx = file_index * entries_per_file
    end_idx = min((file_index + 1) * entries_per_file, len(df))
    chunk = df.iloc[start_idx:end_idx]

    output_lines = [note]  # Start each file with the note

    for _, row in tqdm(chunk.iterrows(), total=len(chunk), desc=f"Processing file {file_index + 1}/{num_files}"):
        edih_name = row.get("EDIH Name", "")
        edih_title = row.get("EDIH Title", "")
        description = row.get("Description (indexed field)", "")
        country = row.get("Country", "")
        contact_name = row.get("Contact name", "")
        contact_phone = row.get("Contact phone", "")
        contact_email = row.get("Contact email", "")
        contact_location = row.get("Contact Location", "")
        seal_status = row.get("EDIH/SoE", "")
        website = row.get("Website", "")

        sectors = parse_engagement_string(row.get("Formatted sectors", ""))
        services = parse_engagement_string(row.get("Formatted services", ""))
        technologies = parse_engagement_string(row.get("Formatted technologies", ""))

        profile = (
            f"EDIH Name: {edih_name}\n"
            f"Title: {edih_title}\n"
            f"Country: {country}\n"
            f"Description: {description}\n"
            f"Contact Person(s): {contact_name}\n"
            f"Phone: {contact_phone}\n"
            f"Email: {contact_email}\n"
            f"Location: {contact_location}\n"
            f"Type: {seal_status}\n"
            f"Website: {website}\n"
            f"Active Sectors: {sectors}\n"
            f"Provided Services: {services}\n"
            f"Technological Focus: {technologies}\n"
            f"{'-'*60}\n"
        )

        output_lines.append(profile)

    # Output file path
    output_file = f"{base_output_name}{file_index + 1}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(output_lines)