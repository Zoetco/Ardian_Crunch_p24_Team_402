import pytesseract
from PIL import Image
import PyPDF2
from PyPDF2 import PdfReader


def extract_text(path):
    raw_text = ""

    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        print(text)

    return raw_text
