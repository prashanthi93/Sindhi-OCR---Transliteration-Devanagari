import pytesseract
from PIL import Image
import fitz  # PyMuPDF

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Define the sindhi_to_devanagari function
def sindhi_to_devanagari(sindhi_text):
    transliteration_dict = {
        'آ': 'आ',
        'ا': 'अ',
        'ب': 'ब',
        'پ': 'प',
        'ت': 'त',
        'ٽ': 'ट',
        'ٹ': 'ट',
        'ث': 'स',
        'ج': 'ज',
        'ڄ': 'ड़',
        'ڊ': 'ड',
        'ڈ': 'ड',
        'ح': 'ह',
        'خ': 'ख',
        'د': 'द',
        'ڍ': 'द',
        'ڏ': 'द',
        'ڌ': 'द',
        'ذ': 'ज़',
        'ر': 'र',
        'ڙ': 'ड़',
        'ز': 'ज़',
        'ژ': 'ज़',
        'س': 'स',
        'ش': 'श',
        'ص': 'स',
        'ض': 'ज़',
        'ع': 'अ',
        'غ': 'ग',
        'ف': 'फ',
        'ق': 'क़',
        'ڪ': 'क',
        'ک': 'क',
        'گ': 'ग',
        'ڳ': 'ग़',
        'ڱ': 'ड़',
        'ل': 'ल',
        'م': 'म',
        'ن': 'न',
        'ڻ': 'ण',
        'ڼ': 'ण',
        'ڽ': 'ण',
        'ه': 'ह',
        'و': 'व',
        'ء': 'अ',
        'ي': 'य',
        '۽': 'य',
        '۾': 'य',
        'ئ': 'अ',
        'ى': 'य',
        'ۏ': 'व',
        'ٻ': 'ब',
        'ٺ': 'ठ',
        'ٿ': 'ट',
        'ڀ': 'ब',
        'ؤ': 'व',
        '٭': 'ऱ',
        'ڃ': 'च',
        'ڨ': 'फ़',
        'ﻁ': 'च',
        'ڪٹ': 'कट',
        '٪': '%',
        '،': ',',
        '؛': ';',
        '؟': '?',
    }
    # Handle unexpected characters and invisible characters
    devanagari_text = ''.join([transliteration_dict.get(char, char) for char in sindhi_text if char.isprintable()])
    return devanagari_text

# Read the PDF file
pdf_path = '/content/sindhi3.pdf'

# Create a PDF document object
pdf_document = fitz.open(pdf_path)

# Initialize an empty string to store the final Devanagari text
final_devanagari_text = ""

# Iterate through pages
for page_number in range(pdf_document.page_count):
    # Extract text from the PDF page
    pdf_page = pdf_document[page_number]
    pdf_text = pdf_page.get_text()

    # Convert the PDF page to an image
    image = pdf_page.get_pixmap()
    image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)

    # Preprocess the image
    image_pil = image_pil.convert('L')  # Convert to grayscale
    image_pil = image_pil.point(lambda x: 0 if x < 128 else 255)  # Thresholding

    # Perform OCR to extract Sindhi text
    sindhi_text = pytesseract.image_to_string(image_pil, lang='snd', config='--psm 6')

    # Convert Sindhi to Devanagari
    devanagari_text = sindhi_to_devanagari(sindhi_text)

    # Append the Devanagari text to the final result
    final_devanagari_text += devanagari_text + '\n'

    # Print both Sindhi and Devanagari text
    print(f'Page {page_number + 1} - Sindhi Text: {sindhi_text}')
    print(f'Page {page_number + 1} - Devanagari Text: {devanagari_text}\n')

# Save Devanagari text to a file (optional)
output_file_path = 'devanagari_output.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(final_devanagari_text)

print(f'Devanagari text saved to {output_file_path}')

# Close the PDF document
pdf_document.close()
