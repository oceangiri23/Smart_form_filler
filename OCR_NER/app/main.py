from NER_predict import get_tags
from OCR import output_text
from text_postprocess import post_process

image_path = "../data/back3.jpg"
ocr_text = output_text(image_path)
ner_text = get_tags(ocr_text)
result = post_process(ner_text)
print(result)