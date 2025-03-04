from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
import shutil
import os
from NER_predict import get_tags
from OCR import output_text
from text_postprocess import post_process

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "chrome-extension://*"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/test")
def test_api():
    return {"message": "It's working!"}

@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        print(f"Uploading file: {file_path}")   
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"Processing image: {file_path}")
        
        # Get OCR text
        ocr_text = output_text(file_path)
        print(f"OCR Output: {ocr_text}")
        
        # Get NER tags
        print("Applying NER tagging...")
        ner_text = get_tags(ocr_text)
        print(f"NER Output: {ner_text}")
        
        # Post-process
        result = post_process(ner_text)
        print(f"Final Result: {result}")
        
        return {"filename": file.filename, "extracted_data": result, "ocr_text": ocr_text, "ner_tags": ner_text, "success": True}
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Print error for debugging
        raise HTTPException(status_code=500, detail={"error": str(e)})