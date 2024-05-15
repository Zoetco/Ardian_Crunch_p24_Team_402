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
                
                pdf.append(text)
                text = ""
                
                    
        return pdf
    except Exception as e:
        print("Une erreur s'est produite lors de l'extraction du texte du PDF :", e)
        return None
    
pdf = extract_text_from_pdf("fichier.pdf")


# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

messages = [
    {"role": "system", "content": "Veuillez ne répondre qu'avec le PDF restructuré. Ne fournissez aucune autre mots ou phrases non présents dans le PDF original."}
]



# Récupérer le contenu du PDF
content = "J'ai perdu la structure de ce PDF. Peux-tu m'aider à recréer les paragraphes de manière logique avec comme règle ultime de ne surtout pas supprimer, modifier ou traduire un seul mot? (ne réponds rien d'autre que le pdf restructutré!)\n"

print(pdf)


print("nombre de pages : ", len(pdf))


newPdf = ""

i = 1
for page in pdf:
    print("page ", i, " : ", len(pdf))
    i += 1
    messages.append({"role": "user", "content": content + page})
    completion = client.chat.completions.create(
        model="MaziyarPanahi/Llama-3-8B-Instruct-32k-v0.1-GGUF",
        messages=messages,
        temperature=0.3,  # Adjust temperature as needed
    )

    # Récupérer la réponse
    newPdf = completion.choices[0].message.content
    
    # on enlève le message de l'utilisateur
    messages.pop(-1)

    split = newPdf.split("\n")
    for s in split:
        print(s)
        print()
                

    
print(newPdf)
