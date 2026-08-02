from fastapi import HTTPException, UploadFile

from app.services.speech import transcribe
from app.services.vision import analyze
from app.services.rag import get_rag_response

from validations import audioValidate, imagevalidate


async def process_ticket(
    audio: UploadFile | None,
    image: UploadFile | None,
    description: str | None,
):
    transcription = None
    image_analysis = None

    # Texte utilisé pour interroger le RAG
    query = description.strip() if description else ""

    # -------------------------
    # Traitement Audio
    # -------------------------
    if audio:

        validate_audio(audio)

        try:
            transcription = transcribe(audio)
            query += f"\n{transcription}"

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la transcription : {str(e)}"
            )

    # -------------------------
    # Traitement Image
    # -------------------------
    if image:

        validate_image(image)

        try:
            image_analysis = analyze(image)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de l'analyse de l'image : {str(e)}"
            )

    # -------------------------
    # Vérification
    # -------------------------
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Veuillez fournir une description ou un fichier audio."
        )

    # -------------------------
    # RAG
    # -------------------------
    try:
        internal_rule = get_rag_response(query)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur RAG : {str(e)}"
        )

    # -------------------------
    # Proposition de statut
    # -------------------------
    rule = internal_rule.lower()

    if "remboursement" in rule:
        status = "Remboursable"

    elif "échange" in rule:
        status = "Échange possible"

    elif "refus" in rule:
        status = "Refusé"

    elif "information introuvable" in rule:
        status = "À vérifier"

    else:
        status = "À vérifier"

    # -------------------------
    # Réponse
    # -------------------------
    return {
        "transcription": transcription,
        "image_analysis": image_analysis,
        "internal_rule": internal_rule,
        "ticket_status": status,
    }