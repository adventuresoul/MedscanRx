from fastapi import APIRouter, UploadFile, File, HTTPException, status, BackgroundTasks, Depends
from app.algorithms.ocr_utils import processImage, extractTextFromImage, processImage
from app.algorithms.nlp_utils import removeStopWords
from app.OAuth import get_current_user
from uuid import uuid4
import os


# Ensure the directory exists
os.makedirs("static", exist_ok=True)
IMAGEDIR = "static"

router = APIRouter(
    prefix="/ocr",
    tags=["ocr"]
)

# Route to upload the file to the server
@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def uploadFile(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    contents = await file.read()
    file_id = str(uuid4())
    file_ext = os.path.splitext(file.filename)[1]  # Get the file extension
    
    if file_ext.lower() != '.jpg':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type. Only .jpg files are allowed.")

    file_name = f"{file_id}{file_ext}"
    
    try:
        file_path = os.path.join(IMAGEDIR, file_name)
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return {"file_id": file_id, "file_name": file_name}
    except OSError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred")


# Router to process the image and extract text
@router.post("/result/{id}", status_code=status.HTTP_200_OK)
async def getTextFromImage(id: str, background_tasks: BackgroundTasks, current_user = Depends(get_current_user)):
    file_name = f"{id}.jpg"  # Assuming only JPG files are handled
    file_path = os.path.join(IMAGEDIR, file_name)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    try:
        processImage(file_path)
        extracted_text = extractTextFromImage(file_path)
        cleaned_text = removeStopWords(extracted_text)
        background_tasks.add_task(cleanup_file, file_path)
        return {"extracted_text": cleaned_text}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing the image")


# a process to clean up the image after extracting the text
def cleanup_file(file_path: str):
    try:
        os.remove(file_path)
    except OSError as e:
        pass
