from chunking import table_aware_chunker 
from extraction import extract_structured_data_robust
import pdfplumber

file_path = "RAG Test PDF for Structured Parsing - RAG Test PDF for Structured Parsing.pdf"
output_file = "table_extraction_test.txt"

# 1. Extract the content
extracted_content = extract_structured_data_robust(file_path)

# 2. Chunk the extracted_content
chunks = table_aware_chunker(extracted_content)

print(len(chunks))
for i in range(len(chunks)):
    print(chunks[i])
    print("-"*50)