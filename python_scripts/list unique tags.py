import pandas as pd
from tiktoken import encoding_for_model

# File paths
csv_path = "EDIH Catalogue_v3.csv"
output_base = "EDIH_Unique_Tags_Part"

# Load data
df = pd.read_csv(csv_path)

# Tokenizer for GPT-4
encoding = encoding_for_model("gpt-4")
MAX_TOKENS = 6000

# Helper functions
def extract_unique_labels(field_series):
    """Extract unique labels (before ' - ' in the string) from a field."""
    labels = set()
    for field in field_series.dropna():
        for item in field.split(","):
            parts = item.strip().rsplit(" - ", 1)
            if len(parts) == 2:
                labels.add(parts[0].strip())
    return sorted(labels)

def count_tokens(text):
    return len(encoding.encode(text))

# Extract unique labels
unique_sectors = extract_unique_labels(df["Formatted sectors"])
unique_services = extract_unique_labels(df["Formatted services"])
unique_technologies = extract_unique_labels(df["Formatted technologies"])

# Sentence templates
sentences = []

if unique_sectors:
    sentence = f"The sectors that an EDIH can be active in are {', '.join(unique_sectors)}."
    sentences.append(sentence)

if unique_services:
    sentence = f"The services that an EDIH can offer are {', '.join(unique_services)}."
    sentences.append(sentence)

if unique_technologies:
    sentence = f"The technologies that an EDIH can focus on are {', '.join(unique_technologies)}."
    sentences.append(sentence)

# Split into chunks of max 6000 tokens, preserving sentence boundaries
chunks = []
current_chunk = ""
current_tokens = 0

for sentence in sentences:
    sentence += "\n\n"
    sentence_tokens = count_tokens(sentence)
    
    if current_tokens + sentence_tokens > MAX_TOKENS and current_chunk:
        chunks.append(current_chunk.strip())
        current_chunk = sentence
        current_tokens = sentence_tokens
    else:
        current_chunk += sentence
        current_tokens += sentence_tokens

if current_chunk:
    chunks.append(current_chunk.strip())

# Write to output files
for i, chunk in enumerate(chunks, start=1):
    with open(f"{output_base}{i}.txt", "w", encoding="utf-8") as f:
        f.write(chunk)

print(f"✅ Done. {len(chunks)} file(s) written.")
