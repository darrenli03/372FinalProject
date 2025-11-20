from text_extractor import extract_pdf_text

def chunk_text(text, max_chars=1000):
    chunks = []
    current = []

    current_len = 0  # track length explicitly (fast + accurate)

    for word in text.split():
        word_len = len(word) + 1  # +1 for space

        # If adding this word makes current chunk exceed limit → push new chunk
        if current_len + word_len > max_chars:
            chunks.append(" ".join(current))
            current = [word]
            current_len = word_len
        else:
            current.append(word)
            current_len += word_len

    # Catch final block
    if current:
        chunks.append(" ".join(current))

    return chunks

chunks = chunk_text(extract_pdf_text("/Users/andyli/Downloads/indexccl.pdf"), max_chars=1000)
print(f"Total chunks: {len(chunks)}")
print(f"First chunk ({len(chunks[0])} chars): {chunks[0]}")

