import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, words
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to check and download the required NLTK data
def download_nltk_data():
    """
    Downloads the necessary NLTK data files if they are not already available.
    """
    try:
        stopwords.words('english')
        words.words()
    except LookupError:
        logger.info("Downloading necessary NLTK data...")
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('words')
        logger.info("NLTK data download complete.")

def removeStopWords(data: str) -> list:
    """
    Filters out the most common English words, stopwords, and non-alphabetic tokens from the given text.

    Args:
        data (str): The input text data to be filtered.

    Returns:
        list: A list of filtered words from the input text.
    """
    # Ensure NLTK data is available
    download_nltk_data()

    # Get a list of common stopwords in English
    stopWords = set(stopwords.words('english'))
    # Get a list of common English words
    commonWords = set(words.words())
    
    # Tokenize the data
    words_list = word_tokenize(data)
    logger.info(f"Original words list: {words_list}")
    
    # Filter out the stop words, common English words, non-alphabetic tokens, and short words
    wordsFiltered = [w for w in words_list if w.lower() not in stopWords and w.isalpha()]
    
    logger.info(f"Filtered words list: {wordsFiltered}")
    return wordsFiltered


