import easyocr
import fitz
import numpy as np
import io
from PIL import Image, ImageDraw



def discern_pdf(pdf_path):
    discern = ""
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    text = page.get_text()
    if text.strip():
        # 'テキスト埋め込み型 PDF'
        discern = "text"
    else:
        # '画像型 PDF'
        discern = "image"
    return discern
    

def pdfocr(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)

    pix = page.get_pixmap(dpi=300)
    image = Image.open(io.BytesIO(pix.tobytes("png")))
    draw = ImageDraw.Draw(image)

    reader = easyocr.Reader(['ja', 'en'])
    results = reader.readtext(np.array(image))

    for result in results:
        p0, p1, p2, p3 = result[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill='red', width=3)
        print(result[1])

    save_path = '/content/PDF1.jpg'
    image.save(save_path)

def pdf_to_text(doc, image_output_path, page_number=0):
    text = ""
    page = doc[page_number]  
    text = page.get_text()
    pix = page.get_pixmap(dpi=200)
    pix.save(image_output_path)
    return text, image_output_path


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