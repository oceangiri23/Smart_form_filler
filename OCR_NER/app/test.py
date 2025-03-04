from NER_predict import get_tags
from OCR import output_text
from text_postprocess import post_process

def main():
    try:
        image_path = "../data/back3.jpg"
        print(f"Processing image: {image_path}")
        
        # Get OCR text
        ocr_text = output_text(image_path)
        print(f"OCR Output: {ocr_text}")
        
        # Get NER tags
        print("Applying NER tagging...")
        ner_text = get_tags(ocr_text)
        print(f"NER Output: {ner_text}")
        
        # Post-process
        result = post_process(ner_text)
        print(f"Final Result: {result}")
        return result
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()