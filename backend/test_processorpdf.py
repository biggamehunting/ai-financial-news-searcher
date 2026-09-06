from pdf_processor import extract_text_from_pdf


file_path = "app/rag/documents/offer_letter_with_ctc_mock.pdf"

text = extract_text_from_pdf(file_path)

print(text)