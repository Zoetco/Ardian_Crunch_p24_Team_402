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
        with open(pdf_path, "rb") as pdf_file:
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

beforePDF = "The following text is unstructured, i.e. the coherence of sentences and paragraphs has been lost. I want you to restructure this text by grouping the paragraphs together, without translating anything.\n"

messages = [
    {
        "role": "system",
        "content": "This is a conversation between Simon and blotbot a friendly chatbot. Blotbot is helpful, kind and honest. Simon is an intelligent and driven individual, but has a mild autistic disorder. Simon is often obsessed with his productivity and efficiency, wanting everything in his life to be perfectly optimized. He leaves no detail to chance and often expects others to be as efficient as he is. He is passionate about text mining in different languages.",
    },
    {
        "role": "user",
        "content": "The following text is unstructured, i.e. the coherence of sentences and paragraphs has been lost. I want you to restructure this text by grouping the paragraphs together, without translating anything.\n\n \n \n OCR Challenge - May 29, 2024  \n CONFIDENTIAL  OCR Challenge  \nCRUNCH UTT 2024  \nINTRODUCTION  \nArdian est le leader européen du private equity. Fondée en 1996, l’entreprise a accumulée depuis \nsa création un très grand nombre de documents confidentiels. Dans une démarche de valorisation \nde ces documents, l’équipe IT est à la recherche d’une solution pour extraire le texte de ces \nDocuments. Pour mieux appréhender cette problématique, l’équipe stagiaire 100% UTTienne du \nprojet ArdianBrowser vous lance ce défi.  \n \nDEFI  \nEnoncé  \n« Extraire le maximum de texte brut de ce PDF, de la manière la mieux \nstructurée possible.  » \nExplication  \nLe « texte brut » ciblé est l’ensemble des mots avec le maximum de ponctuation.\n \n \n OCR Challenge - May 29, 2024  \n CONFIDENTIAL  OCR Challenge  \nCRUNCH UTT 2024  \nINTRODUCTION  \nArdian est le leader européen du private equity. Fondée en 1996, l’entreprise a accumulée depuis \nsa création un très grand nombre de documents confidentiels. Dans une démarche de valorisation \nde ces documents, l’équipe IT est à la recherche d’une solution pour extraire le texte de ces \nDocuments. Pour mieux appréhender cette problématique, l’équipe stagiaire 100% UTTienne du \nprojet ArdianBrowser vous lance ce défi.  \n \nDEFI  \nEnoncé  \n« Extraire le maximum de texte brut de ce PDF, de la manière la mieux \nstructurée possible.  » \nExplication  \nLe « texte brut » ciblé est l’ensemble des mots avec le maximum de ponctuation.",
    },
    {
        "role": "assistant",
        "content": "OCR Challenge - May 29, 2024\n\nCONFIDENTIAL  OCR Challenge\n\nCRUNCH UTT 2024 \n\nINTRODUCTION\n\nArdian est le leader européen du private equity. Fondée en 1996, l’entreprise a accumulée depuis sa création un très grand nombre de documents confidentiels. Dans une démarche de valorisation de ces documents, l’équipe IT est à la recherche d’une solution pour extraire le texte de ces Documents. Pour mieux appréhender cette problématique, l’équipe stagiaire 100% UTTienne du projet ArdianBrowser vous lance ce défi.\n\nDEFI\n\nEnoncé\n\n« Extraire le maximum de texte brut de ce PDF, de la manière la mieux structurée possible. »\n\nExplication\n\nLe « texte brut » ciblé est l’ensemble des mots avec le maximum de ponctuation",
    },
]

print("nombre de pages : ", len(pdf))

newPdf = ""

i = 1
for page in pdf:
    print("page ", i, " : ", len(pdf))
    i += 1
    messages.append({"role": "user", "content": beforePDF + page})
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
