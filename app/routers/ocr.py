from fastapi import APIRouter, UploadFile, File, HTTPException, status, BackgroundTasks, Depends
from app.algorithm_utils.ocr_utils import processImage, extractTextFromImage
from app.OAuth import get_current_user
from app.algorithm_utils import nlp_utils
from app import schemas
from app.algorithm_utils import dbCall
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
@router.post("/files", status_code=status.HTTP_202_ACCEPTED)
async def uploadFile(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """
    Upload a file to the server.

    - **file**: The file to be uploaded.
    - **current_user**: The currently authenticated user.

    Returns:
    - JSON response containing `file_id` and `file_name` if the upload is successful.

    Raises:
    - HTTP 400: If the file type is not supported.
    - HTTP 422: If there is an issue processing the file.
    - HTTP 500: If an unexpected error occurs on the server.
    """
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


# Route to process the image and extract text
@router.post("/files/{id}/text", status_code=status.HTTP_200_OK)
async def getTextFromImage(id: str, background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    """
    Extract text from an uploaded image file.

    - **id**: The unique identifier of the file.
    - **background_tasks**: Background tasks for asynchronous operations.
    - **current_user**: The currently authenticated user.

    Returns:
    - JSON response containing `extracted_text` if the extraction is successful.

    Raises:
    - HTTP 404: If the file is not found on the server.
    - HTTP 500: If an error occurs during text extraction.
    """
    file_name = f"{id}.jpg"  # Assuming only JPG files are handled
    file_path = os.path.join(IMAGEDIR, file_name)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    try:
        processImage(file_path)
        extracted_text = extractTextFromImage(file_path)
        transformed_words = nlp_utils.removeStopWords(' '.join(extracted_text))
        #background_tasks.add_task(cleanup_file, file_path)
        adverse_effects_list = []

        # Fetch adverse effects for each word in transformed_words
        for word in transformed_words:
            adverse_effects = await dbCall.fetch_adverse_effects(word)
            if adverse_effects:
                adverse_effects_list.append(adverse_effects)

        # Add the task to clean up the file in background
        background_tasks.add_task(cleanup_file, file_path)
        return {"Effects": adverse_effects_list}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


# A process to clean up the image after extracting the text
def cleanup_file(file_path: str):
    """
    Remove the file from the server.

    - **file_path**: The path to the file to be removed.
    """
    try:
        os.remove(file_path)
    except OSError:
        pass
