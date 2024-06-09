import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Function to check and download the required NLTK data
def download_nltk_data():
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')


def removeStopWords(data: str):
    """
        Filters the most common English stop words.
        args: data : str
        return: wordsFiltered: list
    """
    # Get a list of common stopwords in English
    stopWords = set(stopwords.words('english'))
    # Tokenize the data
    words = word_tokenize(data)
    # Filter out the stop words
    print("Before filtering: ", words)
    wordsFiltered = [w for w in words if w.lower() not in stopWords and w.isalpha()]
    print("After filtering: ", wordsFiltered)
    return wordsFiltered