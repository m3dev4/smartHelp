from langchain_core.documents import Document


def create_document_chunks(documents):
    chunks = []
    for doc in documents:
        chunk_size = 1000
        for i in range(0, len(doc.page_content), chunk_size):
            chunk = doc.page_content[i : i + chunk_size]
            chunks.append(Document(page_content=chunk, metadata=doc.metadata))
    return chunks

