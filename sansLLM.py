from openai import OpenAI
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
    pdf = []
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
    
contenue = extract_text_from_pdf("fichier.pdf")

def extraire_paragraphe(text):
    paragraphes = []
    # on lit le text lettre par lettre
    paragraphe = ""
    for ligne in text.split("\n"):
        # si la ligne est vide
        if not ligne:
            paragraphes.append(paragraphe)
            paragraphe = ""
            continue
        elif ligne.endswith("."):
            paragraphe += ligne
            paragraphes.append(paragraphe)
            paragraphe = ""
        elif ligne[0].isupper():
            if paragraphe:
                paragraphes.append(paragraphe)
            paragraphe = ligne
        elif not ligne[0].isalpha() and not ligne[0].isdigit() and ligne[0] != " ":
            if paragraphe:
                paragraphes.append(paragraphe)
            paragraphe = ligne
        else:
            paragraphe += ligne + " "
            
    return paragraphes

paragraphes = extraire_paragraphe(contenue)

# on supprime les paragraphes vides
for paragraphe in paragraphes:
    if not paragraphe:
        paragraphes.remove(paragraphe)

for i, paragraphe in enumerate(paragraphes):
    print(paragraphe)
    print("-------------------------------------------------------------\n")



