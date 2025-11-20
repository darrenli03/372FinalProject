import pdfplumber

def extract_pdf_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

#---TESTING---#

PDF_PATH = "files/ccl.pdf"

all_text = extract_pdf_text(PDF_PATH)
print(f"Extracted {len(all_text)} characters from PDF.")
print(all_text[:500])  
