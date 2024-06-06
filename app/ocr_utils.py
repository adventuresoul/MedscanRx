import easyocr
from app.schemas import FilePath

# create an instance of easyocr with supported lang = en and gpu = True[optional]
reader = easyocr.Reader(['en'], gpu=True)

def processImage(img_file_path: FilePath):
    """
        doesn't returns the processed image, inplace operation
    """
    pass



def extractTextFromImage(img_file_path: FilePath):
    """
        Reads image from path and extracts the text using ocr reader object
        args: img_file_path
        return: list of strings
    """
    result = reader.readtext(img_file_path)
    return result


def encodePrdeictions(data):
    """
    FastAPI response encoder cannot handle numpy.int32 objects directly.
    Ensure the returned value is properly serialized before being sent in the response.
    FastAPI response encoder cannot handle directly, specifically a numpy.int32 object. 
    To resolve this, you need to ensure that the returned value from extractTextFromImage 
    is properly serialized before being sent in the response.
    """
    if isinstance(data, (int, float, str, list, dict)):
        response_content = data
    elif hasattr(data, 'tolist'):
        response_content = data.tolist()
    elif isinstance(data, np.integer):
        response_content = int(data)
    elif isinstance(data, np.floating):
        response_content = float(data)
    else:
        response_content = str(data)
    return response_content