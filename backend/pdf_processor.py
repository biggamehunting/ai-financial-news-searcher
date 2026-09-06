import fitz  # PyMuPDF
import fitz


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(doc, start=1):

        content = []

        # Find tables on this page
        tables = page.find_tables()

        table_bboxes = [
            table.bbox
            for table in tables.tables
        ]

        # Extract normal text blocks
        blocks = page.get_text("blocks")

        for block in blocks:
            x0, y0, x1, y1, text, *_ = block

            # Skip text that belongs to a table.
            # We will add the table separately below.
            inside_table = False

            for bbox in table_bboxes:
                tx0, ty0, tx1, ty1 = bbox

                if (
                    x0 >= tx0
                    and y0 >= ty0
                    and x1 <= tx1
                    and y1 <= ty1
                ):
                    inside_table = True
                    break

            if not inside_table and text.strip():
                content.append(text.strip())

        # Extract tables
        for table_number, table in enumerate(
            tables.tables,
            start=1
        ):

            rows = table.extract()

            if not rows:
                continue

            content.append(f"\n[TABLE {table_number}]")

            for row in rows:
                row_text = " | ".join(
                    str(cell or "").strip()
                    for cell in row
                )

                content.append(row_text)

        if content:
            pages.append(
                f"===== PAGE {page_number} =====\n"
                + "\n".join(content)
            )

    doc.close()

    return "\n\n".join(pages)



# def extract_text_from_pdf(file_path: str) -> str:
#     """
#     Extract all text from a PDF, including text contained in tables.
#     """

#     doc = fitz.open(file_path)

#     pages = []

#     for page_number, page in enumerate(doc, start=1):
#         text = page.get_text("text")

#         if text.strip():
#             pages.append(
#                 f"\n--- Page {page_number} ---\n"
#                 f"{text.strip()}"
#             )

#     doc.close()

#     return "\n".join(pages)