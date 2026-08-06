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

Tu es poli, professionnel et naturel dans tes échanges.

Contexte :
{context}

Réclamation :
{input}

Preuve photo :
{photo_evidence}

Consignes :
- Réponds uniquement avec les informations du contexte.
- IMPORTANT : Si aucune photo de preuve n'a été fournie ("Aucune photo fournie"), le statut doit TOUJOURS être "À vérifier" avec un message demandant au client de fournir une photo.
- Si aucune règle ne correspond, réponds :

{{
  "status": "À vérifier",
  "message": "Information introuvable dans le règlement."
}}

- Si une règle correspond ET qu'une photo de preuve a été fournie, retourne UNIQUEMENT un JSON valide sous la forme :

{{
  "status": "<Statut associé dans le règlement>",
  "message": "<Résumé clair de la règle appliquée>"
}}
""")

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)


def get_rag_response(query, image_classification=None):
    if image_classification:
        photo_evidence = f"Photo fournie — Analyse : {json.dumps(image_classification, ensure_ascii=False)}"
    else:
        photo_evidence = "Aucune photo fournie"

    response = rag_chain.invoke({"input": query, "photo_evidence": photo_evidence})
    answer = response["answer"].strip()

    if answer.startswith(("```")):
        answer = answer.replace("```json", "")
        answer = answer.replace("```", "")
        answer = answer.strip()

    return json.loads(answer)
