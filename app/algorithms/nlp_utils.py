import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, words

# Function to check and download the required NLTK data
def download_nltk_data():
    try:
        stopwords.words('english')
        words.words()
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('words')

def removeStopWords(data: str):
    """
        Filters out the most common English words.
        args: data : str
        return: wordsFiltered: list
    """
    # Get a list of common stopwords in English
    stopWords = set(stopwords.words('english'))
    # Get a list of common English words
    commonWords = set(words.words())
    # Tokenize the data
    words_list = word_tokenize(data)
    # Filter out the stop words and common English words
    #print("Before filtering: ", words_list)
    wordsFiltered = [w for w in words_list if w.lower() not in stopWords and w.lower() not in commonWords and w.isalpha() and len(w) > 3]
    #print("After filtering: ", wordsFiltered)
    return wordsFiltered

