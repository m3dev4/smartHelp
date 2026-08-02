from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

from .chunks import create_document_chunks
from .vector_store import create_vector_store

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PDF_PATH = (
    BASE_DIR /
    "smartHelp" /
    "rag" /
    "data" /
    "SmartHelp_Politique_Support_Retour.pdf"
)


@lru_cache
def get_rag_chain():

    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME_OPENROUTER"),
        temperature=0.1,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    chunks = create_document_chunks(documents)

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vector_store = create_vector_store(
        chunks,
        embeddings=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 2}
    )

    prompt = ChatPromptTemplate.from_template(
        """
Tu es un assistant spécialisé dans l'analyse des réclamations clients.

Contexte :
{context}

Réclamation :
{input}

Consignes :
- Réponds uniquement avec les informations du contexte.
- N'invente jamais.
- Si aucune information n'existe, réponds exactement :

Information introuvable dans le règlement.

Réponse :
"""
    )

    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    return create_retrieval_chain(
        retriever,
        document_chain
    )


def get_rag_response(query: str):

    rag_chain = get_rag_chain()

    response = rag_chain.invoke(
        {"input": query}
    )

    return response["answer"]