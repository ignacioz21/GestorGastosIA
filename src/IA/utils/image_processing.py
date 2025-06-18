import pytesseract
from PIL import Image
import pdfplumber
import io

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(file):
    try:
        # Read image directly from file object
        image = Image.open(file)
        
        # Preprocess the image
        image = image.convert('L')  # Convert to grayscale
        text = pytesseract.image_to_string(image, lang="spa")
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")

def extract_text_pdf(file):
    try:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                # Try to extract text directly
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    # Extract images from the page
                    for image in page.images:
                        x0, y0, x1, y1 = image["x0"], image["y0"], image["x1"], image["y1"]
                        cropped_image = page.within_bbox((x0, y0, x1, y1)).to_image()
                        image_bytes = io.BytesIO()
                        cropped_image.save(image_bytes, format="PNG")
                        image_bytes.seek(0)
                        pil_image = Image.open(image_bytes)
                        text += pytesseract.image_to_string(pil_image)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def convert_image_to_supported_format(image):
    try:
        return image.convert("RGB")
    except Exception as e:
        raise Exception(f"Error converting image to supported format: {str(e)}")
