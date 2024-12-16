import PyPDF2
from typing import List

def extract_text_from_pdf(pdf_path) -> List[str]:
    chunks = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            page_chunks = page_text.split('\n\n')
            chunks.extend([chunk.strip() for chunk in page_chunks if chunk.strip()])
    
    return chunks