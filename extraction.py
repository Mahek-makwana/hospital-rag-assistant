import pdfplumber

def extract_structured_data_robust(pdf_path):
    final_output = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # 1. Extract the raw text reliably
            raw_text = page.extract_text() or ""
            
            # 2. Extract tables
            tables = page.find_tables()
            page_tables_md = []
            
            for table in tables:
                table_data = table.extract()
                if table_data:
                    # Create Markdown structure [cite: 41, 48]
                    md_rows = ["| " + " | ".join([(str(c).replace('\n', ' ') if c else "") for c in row]) + " |" for row in table_data]
                    md_table = "\n".join(md_rows)
                    page_tables_md.append(md_table)
            
            # 3. Combine with clear logical separators [cite: 45, 46]
            # This 'interleaving' approach ensures the RAG sees both formats
            # but prioritizes the Markdown structure for table queries.
            page_content = f"--- PAGE {i+1} START ---\n"
            page_content += f"[GENERAL TEXT]\n{raw_text.strip()}\n\n"
            
            if page_tables_md:
                page_content += "[STRUCTURED TABLES]\n"
                page_content += "\n\n".join(page_tables_md)
            
            page_content += f"\n--- PAGE {i+1} END ---"
            final_output.append(page_content)
                
    return "\n\n".join(final_output)

# Run the extraction
if __name__ == "__main__":
    file_path = "RAG Test PDF for Structured Parsing - RAG Test PDF for Structured Parsing.pdf"
    output_file = "table_extraction_test.txt"
    
    # 1. Extract the content
    extracted_content = extract_structured_data_robust(file_path)
    
    # 2. Write to a text file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(extracted_content)
        
    print(f"Success! Content saved to {output_file}")