from openai import OpenAI

import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path

# Chemin vers le fichier PDF
pdf_path = "./fichier.pdf"

# Convertir le PDF en une liste d'images
pages = convert_from_path(pdf_path)

# Initialise une liste pour stocker les paragraphes extraits

pdf = []
contentPDF = ""

# Parcourir chaque page et extraire le texte
for i, page in enumerate(pages):
    # Convertir l'image PIL en tableau numpy pour OpenCV
    img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

    # Conversion en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarisation de l'image
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # OCR avec Pytesseract
    text = pytesseract.image_to_string(threshold_img)
    pdf.append(text) 
    contentPDF += text
    

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Construire les messages pour la requête
messages = [
    {"role": "system", "content": "Veuillez ne répondre qu'avec le PDF restructuré. Ne fournissez aucune autre information ou détail supplémentaire."}
]


# Récupérer le contenu du PDF
content = "J'ai perdu la structure de ce PDF. Peux-tu m'aider à recréer les paragraphes de manière logique avec comme règle ultime de ne surtout pas supprimer, modifier ou traduire un seul mot? (ne réponds rien d'autre que le pdf restructutré!)\n\n"

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
    print(newPdf)
    

    
print(newPdf)
