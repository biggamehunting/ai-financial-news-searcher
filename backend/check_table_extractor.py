from pdf_processor import extract_pdf_elements


PDF_PATH = r"C:\Users\omkar\Downloads\AI\chatbot-app 3\chatbot-app 3\backend\app\rag\documents\offer_letter_with_ctc_mock.pdf"


elements = extract_pdf_elements(PDF_PATH)

for element in elements:

    print("\n" + "=" * 80)

    print("PAGE:", element["page"])
    print("TYPE:", element["type"])

    if element["type"] == "table":
        print("TABLE:", element["table_number"])

    print("-" * 80)
    print(element["content"])