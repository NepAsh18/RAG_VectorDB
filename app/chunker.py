def fixed_chunking(text, size=500, overlap=100):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+size])
        i += size - overlap
    return chunks


def semantic_chunking(text, max_size=700):
    paragraphs = text.split("\n\n")
    chunks, current = [], ""

    for p in paragraphs:
        if len(current) + len(p) <= max_size:
            current += " " + p
        else:
            chunks.append(current.strip())
            current = p

    if current:
        chunks.append(current.strip())

    return chunks
