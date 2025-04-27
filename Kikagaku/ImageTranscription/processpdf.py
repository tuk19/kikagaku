import fitz

def discern_pdf(pdf_path):
    discern = ""
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    text = page.get_text()
    if text.strip():
        discern = 'テキスト埋め込み型 PDF'
    else:
        discern = '画像型 PDF'
    return discern
    

# import fitz
# import easyocr

# def dicrern_pdf(pdf_path, page_number):
#     doc = fitz.open(pdf_path)

#     if isinstance(page_number, int):
#         page_number = [page_number]

#     for page_idx in page_number:
#         if page_idx < 0 or page_idx >= len(doc):
#           print(f"ページ番号 {page_idx+1} は無効です")
#           continue

#         page = doc.load_page(page_idx)
#         text = page.get_text()
#         if text.strip():
#             print(f"{page_idx+1}ページ: テキスト埋め込み型PDF")
#         else:
#             print(f"{page_idx+1}ページ: スキャン画像型PDF")

# pdf_path = '/content/s0914-5b.pdf'
# process_pdf(pdf_path, [-1, 0, 2, 4, 10, 12])