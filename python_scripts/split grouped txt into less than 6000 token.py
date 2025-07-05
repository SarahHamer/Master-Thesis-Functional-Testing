from pathlib import Path
from tiktoken import encoding_for_model

# Files to split
input_files = [
    "EDIH_Country_Grouped.txt",
    "EDIH_Sectors_Grouped.txt",
    "EDIH_Services_Grouped.txt",
    "EDIH_Technologies_Grouped.txt"
]

# Tokenizer setup
encoding = encoding_for_model("gpt-4")
MAX_TOKENS = 6000

def count_tokens(text):
    return len(encoding.encode(text))

def split_text_into_sentences(text):
    # Simple sentence split by period and newline endings (\n)
    sentences = []
    for para in text.split('\n'):
        for sentence in para.split('. '):
            sentence = sentence.strip()
            if sentence:
                if not sentence.endswith('.'):
                    sentence += '.'
                sentences.append(sentence + '\n')
    return sentences

# Split and write files
for file_path in input_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    sentences = split_text_into_sentences(content)

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)
        if current_tokens + sentence_tokens > MAX_TOKENS:
            chunks.append("".join(current_chunk))
            current_chunk = [sentence]
            current_tokens = sentence_tokens
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    if current_chunk:
        chunks.append("".join(current_chunk))

    # Write split chunks to new files
    base_name = Path(file_path).stem
    ext = Path(file_path).suffix
    for i, chunk in enumerate(chunks, 1):
        output_file = f"{base_name}_part{i}{ext}"
        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write(chunk)
