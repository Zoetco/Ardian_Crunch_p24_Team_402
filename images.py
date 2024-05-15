import os
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract



def extract_text(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf = PdfReader(f)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text


def extract_image_text(image_path):
    return pytesseract.image_to_string(Image.open(image_path))


def extract_images_from_pdf(pdf_path, image_folder):
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    image_texts = []

    with open(pdf_path, "rb") as f:
        pdf = PdfReader(f)
        num_pages = len(pdf.pages)

        for page_number in range(num_pages):
            page = pdf.pages[page_number]
            resources = page.get("/Resources", {})
            xObject = resources.get("/XObject", None)

            if xObject:
                for obj in xObject:
                    if xObject[obj].get("/Subtype") == "/Image":
                        size = (xObject[obj]["/Width"], xObject[obj]["/Height"])
                        data = xObject[obj].get_data()
                        mode = "RGB" if xObject[obj]["/ColorSpace"] == "/DeviceRGB" else "P"

                        if "/Filter" in xObject[obj]:
                            if xObject[obj]["/Filter"] == "/FlateDecode":
                                img = Image.frombytes(mode, size, data)
                                img_path = os.path.join(image_folder, f"{os.path.basename(pdf_path)}_page{page_number+1}_img{obj[1:]}.png")
                                img.save(img_path)
                                image_text = extract_image_text(img_path)
                                image_texts.append(image_text)
                            elif xObject[obj]["/Filter"] == "/DCTDecode":
                                img_path = os.path.join(image_folder, f"{os.path.basename(pdf_path)}_page{page_number+1}_img{obj[1:]}.jpg")
                                with open(img_path, "wb") as img_file:
                                    img_file.write(data)
                                image_text = extract_image_text(img_path)
                                image_texts.append(image_text)

    return image_texts


def extract_images_from_pdf(pdf_path, image_folder):
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    image_texts = []

    with open(pdf_path, "rb") as f:
        pdf = PdfReader(f)
        num_pages = len(pdf.pages)

        for page_number in range(num_pages):
            page = pdf.pages[page_number]
            resources = page.get("/Resources", {})
            xObject = resources.get("/XObject", None)

            if xObject:
                for obj in xObject:
                    if xObject[obj].get("/Subtype") == "/Image":
                        size = (xObject[obj]["/Width"], xObject[obj]["/Height"])
                        data = xObject[obj].get_data()
                        mode = "RGB" if xObject[obj]["/ColorSpace"] == "/DeviceRGB" else "P"

                        if "/Filter" in xObject[obj]:
                            if xObject[obj]["/Filter"] == "/FlateDecode":
                                img = Image.frombytes(mode, size, data)
                                img_path = os.path.join(image_folder, f"{os.path.basename(pdf_path)}_page{page_number+1}_img{obj[1:]}.png")
                                img.save(img_path)
                                image_text = extract_image_text(img_path)
                                if image_text:
                                    image_texts.append(image_text)
                            elif xObject[obj]["/Filter"] == "/DCTDecode":
                                img_path = os.path.join(image_folder, f"{os.path.basename(pdf_path)}_page{page_number+1}_img{obj[1:]}.jpg")
                                with open(img_path, "wb") as img_file:
                                    img_file.write(data)
                                image_text = extract_image_text(img_path)
                                if image_text:
                                    image_texts.append(image_text)
    return image_texts


# Exemple d'utilisation
pdf_file_path = "./fichier.pdf"
output_folder = "./dossier_de_sortie"

# Extraction du texte du PDF
pdf_text = extract_text(pdf_file_path)
print("Texte du PDF:")
print(pdf_text)
print()

# Extraction du texte des images avec OCR
image_texts = extract_images_from_pdf(pdf_file_path, output_folder)
print("Texte extrait des images:")
for i, text in enumerate(image_texts):
    print(f"Image {i+1}:")
    print(text)
    print()