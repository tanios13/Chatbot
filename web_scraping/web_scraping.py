import requests
import nltk
import pickle

from helpers.lookups import Path
from helpers.constants import Constants

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

class WebScraper():

    def __init__(self, links_pkl):
        with open(links_pkl.value, 'rb') as file:
            self.links = pickle.load(file)

    def scrape(self):
        """ Scrape the text from the list of links"""

        # Download dependencies
        nltk.download('stopwords')
        nltk.download('punkt')
        
        for link in self.links:
            text = self.extract_text(link)
            cleaned_text = self.clean_text(text)

            # Get the filename
            filename = link.split("/")[3]
            if filename not in ["admission", "international", "aide", "servicesocial", "sio", "sip"]:
                filename = "institutions"
            
            with open(Path.ScrapedText.value + filename + ".txt", 'a') as file:
                file.write(link + "\n")

                for t in cleaned_text:
                    file.write(t + "\n")    

                file.write(Constants.TextSeparator.value)


    def extract_text(self, link):
        """ Extract text from link """
    
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        # Fetch the description of the title
        body = soup.find_all("p")
        paragraphs = []
        for paragraph in body:
            paragraphs.append(paragraph.text)

        return paragraphs

    def clean_text(self, data):
        """ Clean the list of strings """

        # Get the list of stopwords
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
