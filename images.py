import PyPDF2
import fitz
from PIL import Image
import pytesseract
import io

# pip install PyMuPDF pytesseract pillow

def extract_text_from_image(image):
    try:
        # Utiliser Tesseract pour extraire le texte de l'image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print("Une erreur s'est produite lors de l'extraction du texte de l'image :", e)
        return None

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # Ouvrir le fichier PDF en mode lecture binaire
        with open(pdf_path, 'rb') as pdf_file:
            # Initialiser un objet PdfReader
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Parcourir toutes les pages du PDF
            for page_num in range(len(pdf_reader.pages)):
                # Extraire le texte de chaque page
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                
                # Extraire le texte des images de la page
                doc = fitz.open(pdf_path)
                page_images = doc[page_num].get_images(full=True)
                for img_index, img_info in enumerate(page_images):
                    xref = img_info[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    text += extract_text_from_image(image)
                    
        return text
    except Exception as e:
        print("Une erreur s'est produite lors de l'extraction du texte du PDF :", e)
        return None

# Exemple d'utilisation
pdf_path = "./fichier.pdf"
texte_extrait = extract_text_from_pdf(pdf_path)
if texte_extrait:
    print(texte_extrait)
else:
    print("Impossible d'extraire le texte du PDF.")


