import os
import tiktoken

# List of files to analyze
file_list = [
    "EDIH_Catalogue_part1.txt",
    "EDIH_Catalogue_part2.txt",
    "EDIH_Catalogue_part3.txt",
    "EDIH_Catalogue_part4.txt",
    "EDIH_Catalogue_part5.txt",
    "EDIH_Sectors_Grouped.txt",
    "EDIH_Services_Grouped.txt",
    "EDIH_Technologies_Grouped.txt"
]

# Choose encoding compatible with GPT-4
encoding = tiktoken.encoding_for_model("gpt-4")

# Function to count tokens in a text string
def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

# Count tokens in each file
print("Token counts for each file:\n" + "-"*40)
for filename in file_list:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            token_count = count_tokens(content)
            print(f"{filename}: {token_count} tokens")
    else:
        print(f"{filename}: File not found")
