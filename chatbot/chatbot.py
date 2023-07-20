import os
import pinecone

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings

from helpers.constants import Constants

class Chatbot():
    def __init__(self, index_name, create_index):
        """
        
        Arguments:
        index_name : index store name in the pinecone
        create_vectorstore : True if create new index, False if from existing index
        """

        self.index_name = index_name
        self.init_vectorstore = False
        self.embeddings = OpenAIEmbeddings()

        self._init_pinecone(create_index)


    def add_dir(self, dir_path, separator):
        # Load and split the documents in the dir
        docs = self._load_dir(dir_path, separator)

        # Add them to the vectorstore
        self._store_docs(docs)

    def add_pdf(self, pdf_path):
        pass

    
#----------------------------------------------------------------------------HELPERS----------------------------------------------------------------

    def _init_pinecone(self, create_index):
        # init the pinecone
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp-free")
        
        # Check pinecone version
        version_info = pinecone.info.version()
        server_version = ".".join(version_info.server.split(".")[:2])
        client_version = ".".join(version_info.client.split(".")[:2])
        #assert client_version == server_version, "Please upgrade pinecone-client."

        if create_index:
            # Check if index already exists
            if self.index_name in pinecone.list_indexes():
                pinecone.delete_index(self.index_name)

            # Create index
            pinecone.create_index(self.index_name, dimension=Constants.OpenAIEmbeddingsDimension.value)



    def _store_docs(self, docs):
        if self.init_vectorstore:
            index = pinecone.Index(self.index_name)
            self.vectorstore = Pinecone(index, embedding_function=self.embeddings.embed_query, text_key="text")
            self.vectorstore.add_texts([doc.page_content for doc in docs])
        else:
            # If the index isn't initiliazed initialize it with the documents
            self.vectorstore = Pinecone.from_documents(documents=docs, embedding=self.embeddings, index_name=self.index_name)




#-----------------------------------------------------------------------TEXT DIR HANDLER-----------------------------------------------------------------------------

    def _load_dir(self, dir_path, separator):
        """
        Load and split the documents in the dir using the separator for each txt in the dir

        """

        docs = []

        c_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 3000,
            chunk_overlap = 200,
            separators=separator + "\n",
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

    def _load_pdf(pdf):
        pass