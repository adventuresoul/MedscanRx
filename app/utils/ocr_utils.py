import easyocr
from app.schemas import FilePath

# create an instance of easyocr with supported lang = en and gpu = True[optional]
reader = easyocr.Reader(['en'], gpu=False)


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
    # do the processing for returning only words not numbers such as co-ordinates
    words = []
    for ext in result:
        words.append(ext[1])
    return ' '.join(words)
    

