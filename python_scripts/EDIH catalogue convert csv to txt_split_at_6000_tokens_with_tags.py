import pandas as pd
from tqdm import tqdm
from tiktoken import encoding_for_model

# Define input/output paths
csv_path = 'EDIH Catalogue_v3.csv'
base_output_name = '6000_token_EDIH_Catalogue_with_tags_part'

# Load CSV
df = pd.read_csv(csv_path)

# Tokenizer for GPT-4
encoding = encoding_for_model("gpt-4")
MAX_TOKENS = 6000

# Mapping numeric engagement to text
engagement_map = {
    1: "very low involvement",
    2: "low involvement",
    3: "moderate involvement",
    4: "high involvement",
    5: "very high involvement"
}

def parse_engagement_string(field):
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

def parse_engagement_tags(field):
    if pd.isna(field):
        return []
    tags = []
    items = field.split(",")
    for item in items:
        parts = item.strip().rsplit(" - ", 1)
        if len(parts) == 2:
            name = parts[0].strip()
            tags.append(name)
    return tags

# Explanatory note
note = (
    "NOTE:\n"
    "The 'Type' field indicates whether the EDIH has received a 'Seal of Excellence', is an EDIH, or a DIH.\n"
    "- 'EDIH' means the hub is part of the funded European Digital Innovation Hub network. It is co-funded by the European Commission and Member States/Associated Countries.\n"
    "- 'Seal of Excellence' means the hub was evaluated positively in a European competitive call but is funded exclusively by national or regional resources.\n"
    "- 'DIH' means digital innovation hubs with similar activities to EDIHs but not connected to the network.\n"
    "------------------------------------------------------------\n\n"
)

# Helper to count tokens
def count_tokens(text):
    return len(encoding.encode(text))

# Start file output
file_index = 1
current_tokens = count_tokens(note)
output_lines = [note]

for _, row in tqdm(df.iterrows(), total=len(df), desc="Splitting by token count"):
    profile_lines = []

    def append_if_present(label, value):
        if pd.notna(value) and str(value).strip() != "":
            profile_lines.append(f"{label}: {value.strip()}\n")

    append_if_present("EDIH Name", row.get("EDIH Name", ""))
    append_if_present("Title", row.get("EDIH Title", ""))
    append_if_present("Country", row.get("Country", ""))
    append_if_present("Description", row.get("Description (indexed field)", ""))
    append_if_present("Contact Person(s)", row.get("Contact name", ""))
    append_if_present("Phone", row.get("Contact phone", ""))
    append_if_present("Email", row.get("Contact email", ""))
    append_if_present("Location", row.get("Contact Location", ""))
    append_if_present("Type", row.get("EDIH/SoE", ""))
    append_if_present("Website", row.get("Website", ""))

    sectors = parse_engagement_string(row.get("Formatted sectors", ""))
    services = parse_engagement_string(row.get("Formatted services", ""))
    technologies = parse_engagement_string(row.get("Formatted technologies", ""))

    if sectors:
        append_if_present("Active Sectors", sectors)
    if services:
        append_if_present("Provided Services", services)
    if technologies:
        append_if_present("Technological Focus", technologies)

    # Construct tags line
    tags = []
    country = row.get("Country", "").strip()
    if country:
        tags.append(f"Country:{country}")
    tags += [f"Sector:{s}" for s in parse_engagement_tags(row.get("Formatted sectors", ""))]
    tags += [f"Service:{s}" for s in parse_engagement_tags(row.get("Formatted services", ""))]
    tags += [f"Technology:{s}" for s in parse_engagement_tags(row.get("Formatted technologies", ""))]

    if tags:
        profile_lines.append("Tags: " + "; ".join(tags) + "\n")

    profile_lines.append(f"{'-'*60}\n")

    profile_text = "".join(profile_lines)
    profile_tokens = count_tokens(profile_text)

    if current_tokens + profile_tokens > MAX_TOKENS:
        output_file = f"{base_output_name}{file_index}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(output_lines)

        file_index += 1
        output_lines = [note]
        current_tokens = count_tokens(note)

    output_lines.append(profile_text)
    current_tokens += profile_tokens

# Save remaining
if output_lines:
    output_file = f"{base_output_name}{file_index}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(output_lines)
