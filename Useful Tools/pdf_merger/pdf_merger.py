from pypdf import PdfWriter

# 1. Create a PDF writer object
merger = PdfWriter()

# 2. Create a list of the PDF files you want to merge (in order)
pdfs_to_merge = ["document1.pdf", "document2.pdf"]

# 3. Loop through the list and append them to the merger
for pdf in pdfs_to_merge:
    merger.append(pdf)

# 4. Save the final merged document
merger.write("merged_document.pdf")
merger.close()

print("PDFs merged successfully!")