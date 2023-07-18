# Langchain-chat-with-your-data

## Document Loading
There exist a lot of document loading APIs in the langchain library:
- Youtube video loader,
- PDF loader,
- Directory loader,
- Webpage loader...

After loading the documents, we need to split it in smaller chunks. This is relevant because when we are doing the retrieval augmented generation, you need to retrieve the piece of content that are only relevant.

See full [documentation](https://python.langchain.com/docs/modules/data_connection/document_loaders.html)

## Document Splitting
We have to be careful when we split into chunks to keep the context:
    e.g. The toyota camry has a head snapping  80HP and an eight speed automatic transmission
    Chunk 1: The toyota camry has a head snapping
    Chunk 2: 80HP and an eight speed automatic transmission

There is a lot of types of splitters.

See full [documentation](https://python.langchain.com/docs/modules/data_connection/document_transformers/)