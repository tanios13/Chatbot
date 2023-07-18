from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

from helpers.constants import Constants

import os

class Chatbot():
    def __init__(self):
        pass

    def load_dir(dir_path, separator):
        """
        Load and split the documents in the dir using the separator for each txt in the dir
        
        """
        docs = []

        c_splitter = CharacterTextSplitter(
            chunk_size = 10,
            chunk_overlap = 5,
            separator=separator.value
        )

        # Iterate over the scraped data
        for filename in os.listdir(dir_path):
            if filename.endswith(".txt"):  # Filter only text files
                file_path = os.path.join(dir_path, filename)

                # Load the text file
                loader = TextLoader(file_path)
                text = loader.load()

                # Split into chunks
                docs.append(c_splitter.split_documents(text))

        return docs

    def load_pdf(pdf):
        pass