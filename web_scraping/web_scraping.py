import requests
import nltk

from helpers.lookups import Path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


def web_scrape(links):
    """ Scrape the text from the list of links"""

    # Download dependencies
    nltk.download('stopwords')
    nltk.download('punkt')

    # Open the file in write mode to clean it
    with open(Path.ScrapedText.value, 'w') as file:
        file.write('')  # Write an empty string to clear the file

        
    for link in links:
        text = extract_text(link)
        cleaned_text = clean_text(text)

        with open(Path.ScrapedText.value, 'a') as file:
            file.write(link + "\n")

            for t in cleaned_text:
                file.write(t + "\n")    

            file.write("------------------------------------------------------\n")

    file.close()


def extract_text(link):
    """ Extract text from link """
    
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")

    # Fetch the description of the title
    body = soup.find_all("p")
    paragraphs = []
    for paragraph in body:
        paragraphs.append(paragraph.text)

    return paragraphs

def clean_text(data):
    """ Clean the list of strings """

    # Get the list stopwords
    stop_words = set(stopwords.words('english'))

    cleaned_data = []
    for sentence in data:
        # Tokenize the sentence
        tokens = word_tokenize(sentence)
        # Remove stopwords and convert to lowercase
        cleaned_tokens = [token for token in tokens if token.lower() not in stop_words]
        # Join the cleaned tokens back into a sentence
        cleaned_sentence = " ".join(cleaned_tokens)
        # Remove empty sentences
        if cleaned_sentence:
            cleaned_data.append(cleaned_sentence)
    
    return cleaned_data
