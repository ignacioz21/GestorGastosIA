import pytesseract
from PIL import Image
import io
import fitz

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(file):
    try:
        img = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(img)
        print("Extracted text:", text)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        return None
    

def extract_text_pdf(file):
    try:
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text += page.get_text()
        print("Extracted text from PDF:", text)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None
