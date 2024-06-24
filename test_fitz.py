import fitz  # PyMuPDF

# Ensure the file path is correct
pdf_path = 'path_to_your_pdf_file.pdf'

doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text()
print(text)
