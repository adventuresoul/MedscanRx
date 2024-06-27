import easyocr
from app.schemas import FilePath
from app.algorithms.imgProc_utils import ImagePreprocesser

# create an instance of easyocr with supported lang = en and gpu = True[optional]
reader = easyocr.Reader(['en'], gpu=True)


def processImage(img_file_path: FilePath):
    """
        doesn't returns the processed image, inplace operation
    """
    obj = ImagePreprocesser(img_file_path)
    obj.processImage()
    

def extractTextFromImage(img_file_path: FilePath):
    """
        Reads image from path and extracts the text using ocr reader object
        args: img_file_path
        return: list of strings
    """
    #print("I am inside extract Text from Image")
    result = reader.readtext(img_file_path)
    words = []
    for ext in result:
        words.append(ext[1])
    return ' '.join(words)
    

