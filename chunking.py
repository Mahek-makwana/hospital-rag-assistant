from langchain_text_splitters import RecursiveCharacterTextSplitter

def table_aware_chunker(text, chunk_size=1000, chunk_overlap=100):
    # Split text by our custom [STRUCTURED TABLES] tags
    # This separates clean Markdown tables from general prose
    parts = text.split("[STRUCTURED TABLES]")
    final_chunks = []
    
    # Standard text splitter for non-table parts
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]  # Paragraph -> Line -> Sentence
    )
    
    for part in parts:
        # If the part contains Markdown table syntax, we treat it as an atomic unit
        if "|" in part and "---" in part:
            final_chunks.append(part.strip())
        else:
            # Apply standard recursive splitting to [GENERAL TEXT]
            final_chunks.extend(text_splitter.split_text(part))
            
    return final_chunks