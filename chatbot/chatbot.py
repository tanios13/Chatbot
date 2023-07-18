import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


class Chatbot():
    def __init__(self):
        self.vectorstore = Chroma("usj_store", OpenAIEmbeddings())


    def store_docs(self, docs):
        self.vectorstore.add_documents(documents=docs)


    def add_dir(self, dir_path, separator):
        # Load and split the documents in the dir
        docs = self.load_dir(dir_path, separator)

        # Add them to the vectorstore
        self.store_docs(docs)

#-----------------------------------------------------------------------TEXT DIR HANDLER-----------------------------------------------------------------------------

    # TODO see how to remove prints from splitting
    def load_dir(self, dir_path, separator):
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
        for filename in os.listdir(dir_path.value):
            if filename.endswith(".txt"):  # Filter only text files
                file_path = os.path.join(dir_path.value, filename)

                # Load the text file
                loader = TextLoader(file_path)
                text = loader.load()

                # Split into chunks
                docs.extend(c_splitter.split_documents(text))

        return docs


#------------------------------------------------------------------------PDF HANDLER--------------------------------------------------------------------------

    def load_pdf(pdf):
        pass