from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from .chunks import create_document_chunks
from .vector_store import create_vector_store
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PDF_PATH = (
    BASE_DIR / "smartHelp" / "rag" / "data" / "SmartHelp_Politique_Support_Retour.pdf"
)

load_dotenv()

MODEL_NAME_OPENROUTER = os.getenv("MODEL_NAME_OPENROUTER")
OPENROUTER_API = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    model=MODEL_NAME_OPENROUTER,
    temperature=0.1,
    api_key=OPENROUTER_API,
    base_url="https://openrouter.ai/api/v1",
)


# ---------------------------- Chargement du document ----------------------------------------
loader = PyPDFLoader(PDF_PATH)

documents = loader.load()

# ---------------------------- Chunks -----------------------------
chunkDoc = create_document_chunks(documents)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorStore = create_vector_store(chunkDoc, embeddings=embeddings)


# ---------------------------- Récupération des informations ----------------------------------------
retriever = vectorStore.as_retriever(search_kwargs={"k": 2})

# ---------------------------- Création de la chaîne de récupération ----------------------------------------
prompt = ChatPromptTemplate.from_template("""
Tu es un assistant spécialisé dans l'analyse des réclamations clients.

Contexte :
{context}

Réclamation :
{input}

Consignes :
- Réponds uniquement avec les informations du contexte.
- Si aucune règle ne correspond, réponds :

{{
  "status": "À vérifier",
  "message": "Information introuvable dans le règlement."
}}

- Si une règle correspond, retourne UNIQUEMENT un JSON valide sous la forme :

{{
  "status": "<Statut associé dans le règlement>",
  "message": "<Résumé clair de la règle appliquée>"
}}
""")

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)


def get_rag_response(query):
    response = rag_chain.invoke({"input": query})
    answer = response["answer"].strip()

    if answer.startswith(("```")):
        answer = answer.replace("```json", "")
        answer = answer.replace("```", "")
        answer = answer.strip()

    return json.loads(answer)
