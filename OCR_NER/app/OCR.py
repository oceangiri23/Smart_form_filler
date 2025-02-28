import pytesseract
import cv2
import os
import re
import string

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
custom_config = r'--oem 3 --psm 6'


def split_token(token):

    token = re.sub(r'([a-z])([A-Z])', r'\1 \2', token)
    parts = []
    for part in token.split():
        parts.extend(re.findall(r'[A-Za-z]+|\d+', part))
    return parts

def clean_text(text):

    raw_tokens = text.split()
    cleaned_tokens = []
    for token in raw_tokens:
        token = token.strip(string.punctuation)
        if not token:
            continue
        sub_tokens = split_token(token)
        cleaned_tokens.extend([sub for sub in sub_tokens if sub])
    return cleaned_tokens



def output_text(image_path):
    image_back = cv2.imread(image_path)
    back_text = pytesseract.image_to_string(image_back, config=custom_config)
    unwanted = ";:{}[]()|,~=+_-—.«*‘“"
    translator = str.maketrans('', '', unwanted)
    cleaned_text = back_text.translate(translator)

    try:
        try :
            start_index = cleaned_text.lower().index("details")
            truncated_text = cleaned_text[start_index:]

        except (ValueError, StopIteration):
            start_index = cleaned_text.lower().index("government")
            truncated_text = cleaned_text[start_index:]


        split_text = truncated_text.split()


        ward_index = next(i for i, word in enumerate(split_text) if word.lower() == 'ward')


        result_words = split_text[:ward_index +25]
        result = ' '.join(result_words)
    except (ValueError, StopIteration):
        result = cleaned_text

    cleaned_tokens = clean_text(result)
    sentence = " ".join(cleaned_tokens)
    return sentence


