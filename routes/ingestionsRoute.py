from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from validations.audioValidate import validate_audio
from validations.imageValidate import validate_image
from utils.files_manager import save_file_temp
from utils.file_manager_img import save_file_temp_img
from services.whisperService import transcriber
from services.vitService import image_classifier
from rag.rag import get_rag_response
from typing import Optional

router = APIRouter(prefix="/ingestions", tags=["Ingestions"])


@router.post("/support-ticket")
async def create_ingestion_from_support_ticket(
    audio: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    description: str | None = Form(None),
):
    await validate_audio(audio)
    validate_image(image)
    audio_path = save_file_temp(audio)
    image_path = save_file_temp_img(image)

    audio_transcription = transcriber(audio_path) if audio_path else None
    image_classification = image_classifier(image_path) if image_path else None

    userTyping = (audio_transcription["text"] if audio_transcription else description) or description
    rag_result = get_rag_response(userTyping, image_classification) if userTyping else None


    return {
        "transcription": userTyping,
        "defect_detected": image_classification,
        "policy_rule_applied": rag_result["message"] if rag_result else None,
        "diagnostic_status": rag_result["status"] if rag_result else None,
    }
