import os
import pinecone

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from helpers.constants import Constants

class Chatbot():
    def __init__(self, model_name, index_name, existing_index):
        """
        
        Arguments:
        index_name : index store name in the pinecone
        create_vectorstore : True if create new index, False if from existing index
        """

        self.index_name = index_name
        self._init_vectorstore = False
        self._embeddings = OpenAIEmbeddings()
        self.vectorstore = self._init_pinecone(existing_index)
        self._llm = ChatOpenAI(model_name=model_name, temperature=0)
        self._memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )


    def add_dir(self, dir_path, separator):
        # Load and split the documents in the dir
        docs = self._load_dir(dir_path, separator)

        # Add them to the vectorstore
        self._store_docs(docs)

    def add_pdf(self, pdf_path):
        pass


    def answer_question(self, question):
        if self.vectorstore == None:
            return "Cannot answer from empty Vector Store is Empty"

        else:
            qa_chain = ConversationalRetrievalChain.from_llm(
                        llm=self._llm,
                        retriever=self.vectorstore.as_retriever(),
                        memory=self._memory
                    )
            
            return qa_chain({"question": question})
        
    def clear_history(self):
        self._memory.clear()
    
#----------------------------------------------------------------------------HELPERS----------------------------------------------------------------

    def _init_pinecone(self, existing_index):
        # init the pinecone
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp-free")
        
        # Check pinecone version
        #version_info = pinecone.info.version()
        #server_version = ".".join(version_info.server.split(".")[:2])
        #client_version = ".".join(version_info.client.split(".")[:2])
        #assert client_version == server_version, "Please upgrade pinecone-client."

        if not existing_index:
            # Check if index already exists
            if self.index_name in pinecone.list_indexes():
                pinecone.delete_index(self.index_name)

            # Create index
            pinecone.create_index(self.index_name, dimension=Constants.OpenAIEmbeddingsDimension.value)

            return None

        elif self.index_name in pinecone.list_indexes():
            self._init_pinecone = True
            return Pinecone.from_existing_index(self.index_name, self._embeddings, "text")



    def _store_docs(self, docs):
        if self._init_vectorstore:
            # If the vector store is not empty and thus already initialized
            index = pinecone.Index(self.index_name)
            self.vectorstore = Pinecone(index, embedding_function=self._embeddings.embed_query, text_key="text")
            self.vectorstore.add_documents(documents=docs)
        else:
            # If the index isn't initiliazed initialize it with the documents
            self.vectorstore = Pinecone.from_documents(documents=docs, embedding=self._embeddings, index_name=self.index_name)
            self._init_pinecone = True



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
            keep_separator=False
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