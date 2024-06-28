import easyocr
from app.schemas import FilePath
from app.algorithm_utils.imgProc_utils import ImagePreprocesser

# Initialize EasyOCR reader with English language support and GPU acceleration if available
reader = easyocr.Reader(['en'], gpu=True)

def processImage(img_file_path: FilePath):
    """
    Process the image in-place using ImagePreprocesser.

    Args:
        img_file_path (FilePath): Path to the image file.

    Returns:
        None
    """
    obj = ImagePreprocesser(img_file_path)
    obj.processImage()

def extractTextFromImage(img_file_path: FilePath):
    """
    Extract text from an image using EasyOCR.

    Args:
        img_file_path (FilePath): Path to the image file.

    Returns:
        str: Extracted text from the image.
    """
    try:
        result = reader.readtext(img_file_path)
        words = [ext[1] for ext in result]
        return words
    except Exception as e:
        # Handle specific exceptions for EasyOCR or image reading errors
        raise RuntimeError(f"Error extracting text from image: {str(e)}")

# Example usage:
# img_path = 'path_to_your_image.jpg'
# processImage(img_path)
# extracted_text = extractTextFromImage(img_path)
# print(extracted_text)
